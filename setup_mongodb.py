"""
Setup script to populate MongoDB with StansBooth knowledge base
Run this once to initialize the database
"""

from mongodb_handler import MongoDBHandler

def setup_knowledge_base():
    """Initialize MongoDB with StansBooth knowledge base"""
    print("=" * 60)
    print("StansBooth Knowledge Base Setup")
    print("=" * 60)
    print()

    # Initialize MongoDB handler
    print("1. Connecting to MongoDB...")
    mongo = MongoDBHandler()

    if not mongo.is_connected():
        print()
        print("⚠️  MongoDB is not running!")
        print()
        print("Please ensure MongoDB is installed and running:")
        print("  - Download: https://www.mongodb.com/try/download/community")
        print("  - Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas")
        print()
        print("After installing, start MongoDB service and run this script again.")
        return False

    # Load knowledge base
    print("2. Loading knowledge base from JSON file...")
    success = mongo.load_knowledge_from_file("knowledge_base.json")

    if success:
        print()
        print("=" * 60)
        print("✓ Setup Complete!")
        print("=" * 60)
        print()
        print("Your chatbot now has access to:")
        print("  • Company information")
        print("  • Services and features")
        print("  • Pricing plans")
        print("  • FAQs")
        print("  • Trading sessions")
        print("  • And more!")
        print()
        print("You can now run: python app.py")
    else:
        print()
        print("⚠️  Setup failed. Please check the error messages above.")

    mongo.close()
    return success

if __name__ == "__main__":
    setup_knowledge_base()
