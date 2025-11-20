"""
MongoDB Handler for StansBooth AI Chatbot
Manages knowledge base storage and retrieval
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import json
import os

class MongoDBHandler:
    def __init__(self, connection_string=None, db_name="stansbooth_db"):
        """
        Initialize MongoDB connection

        Args:
            connection_string: MongoDB connection URI (defaults to localhost)
            db_name: Database name
        """
        if connection_string is None:
            # Default to localhost MongoDB
            connection_string = "mongodb://localhost:27017/"

        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[db_name]
            self.knowledge_collection = self.db["knowledge_base"]
            print(f"[OK] Connected to MongoDB: {db_name}")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"[WARNING] MongoDB connection failed: {e}")
            print("Running in fallback mode without database")
            self.client = None
            self.db = None
            self.knowledge_collection = None

    def is_connected(self):
        """Check if MongoDB is connected"""
        return self.client is not None

    def load_knowledge_from_file(self, file_path="knowledge_base.json"):
        """Load knowledge base from JSON file into MongoDB"""
        if not self.is_connected():
            print("[WARNING] Cannot load to MongoDB: Not connected")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                knowledge_data = json.load(f)

            # Clear existing data
            self.knowledge_collection.delete_many({})

            # Insert company info
            self.knowledge_collection.insert_one({
                "type": "company",
                "data": knowledge_data.get("company", {})
            })

            # Insert social media
            self.knowledge_collection.insert_one({
                "type": "social_media",
                "data": knowledge_data.get("social_media", {})
            })

            # Insert services
            for service in knowledge_data.get("services", []):
                self.knowledge_collection.insert_one({
                    "type": "service",
                    "name": service["name"],
                    "data": service
                })

            # Insert features
            for feature in knowledge_data.get("features", []):
                self.knowledge_collection.insert_one({
                    "type": "feature",
                    "name": feature["name"],
                    "data": feature
                })

            # Insert pricing plans
            for plan in knowledge_data.get("pricing_plans", []):
                self.knowledge_collection.insert_one({
                    "type": "pricing_plan",
                    "name": plan["name"],
                    "data": plan
                })

            # Insert trading sessions
            for session in knowledge_data.get("trading_sessions", []):
                self.knowledge_collection.insert_one({
                    "type": "trading_session",
                    "name": session["name"],
                    "data": session
                })

            # Insert FAQs
            for faq in knowledge_data.get("faqs", []):
                self.knowledge_collection.insert_one({
                    "type": "faq",
                    "question": faq["question"],
                    "data": faq
                })

            # Insert vision
            self.knowledge_collection.insert_one({
                "type": "vision",
                "data": {"text": knowledge_data.get("vision", "")}
            })

            # Insert why_choose_stansbooth
            for reason in knowledge_data.get("why_choose_stansbooth", []):
                self.knowledge_collection.insert_one({
                    "type": "why_choose",
                    "title": reason["title"],
                    "data": reason
                })

            # Insert blogs
            for blog in knowledge_data.get("blogs", []):
                self.knowledge_collection.insert_one({
                    "type": "blog",
                    "title": blog["title"],
                    "data": blog
                })

            count = self.knowledge_collection.count_documents({})
            print(f"[OK] Loaded {count} knowledge base entries into MongoDB")
            return True

        except Exception as e:
            print(f"[ERROR] Error loading knowledge base: {e}")
            return False

    def search_knowledge(self, query, limit=5):
        """
        Search knowledge base for relevant information

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of relevant knowledge base entries
        """
        if not self.is_connected():
            return []

        query_lower = query.lower()
        results = []

        # Search in FAQs
        faqs = self.knowledge_collection.find({
            "type": "faq",
            "$or": [
                {"question": {"$regex": query_lower, "$options": "i"}},
                {"data.answer": {"$regex": query_lower, "$options": "i"}}
            ]
        }).limit(limit)
        results.extend(list(faqs))

        # Search in services
        services = self.knowledge_collection.find({
            "type": "service",
            "$or": [
                {"name": {"$regex": query_lower, "$options": "i"}},
                {"data.description": {"$regex": query_lower, "$options": "i"}}
            ]
        }).limit(limit)
        results.extend(list(services))

        # Search in features
        features = self.knowledge_collection.find({
            "type": "feature",
            "$or": [
                {"name": {"$regex": query_lower, "$options": "i"}},
                {"data.description": {"$regex": query_lower, "$options": "i"}}
            ]
        }).limit(limit)
        results.extend(list(features))

        # Search in pricing plans
        if any(word in query_lower for word in ['price', 'plan', 'cost', 'pricing', 'professional', 'business', 'premium', 'starter', 'enterprise']):
            plans = self.knowledge_collection.find({"type": "pricing_plan"}).limit(limit)
            results.extend(list(plans))

        return results[:limit]

    def get_all_pricing_plans(self):
        """Get all pricing plans"""
        if not self.is_connected():
            return []

        plans = self.knowledge_collection.find({"type": "pricing_plan"})
        return list(plans)

    def get_company_info(self):
        """Get company information"""
        if not self.is_connected():
            return {}

        result = self.knowledge_collection.find_one({"type": "company"})
        return result.get("data", {}) if result else {}

    def get_all_services(self):
        """Get all services"""
        if not self.is_connected():
            return []

        services = self.knowledge_collection.find({"type": "service"})
        return list(services)

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("[OK] MongoDB connection closed")
