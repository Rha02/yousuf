from driver.driver import MongoDB
import os

def main():
    print("Reading environment variables...")
    mongodb_uri = os.getenv("MONGODB_URI")
    if (mongodb_uri is None):
        print("MONGODB_URI not found in environment variables")
        exit(1)

    dbname = os.getenv("DB_NAME")

    dbconn = MongoDB(mongodb_uri, dbname=dbname)

    # Clear the database
    print("Clearing MongoDB database...")
    dbconn.client.drop_database(dbname)

    print("Setting up MongoDB database...")

    # Create a validation schema for the users collection
    user_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["first_name", "last_name", "email", "password"],
            "properties": {
                "first_name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "last_name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "email": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }

    dbconn.db.create_collection("users", validator=user_validator)

    # Add a unique index on the email field
    dbconn.db.users.create_index("email", unique=True)

    print("Created users collection")

    # Create a validation schema for the chats collection
    chat_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "user_id"],
            "properties": {
                "title": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "user_id": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }

    dbconn.db.create_collection("chats", validator=chat_validator)

    print("Created chats collection")
    print("Database setup complete")

