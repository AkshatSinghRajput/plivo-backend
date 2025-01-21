import pymongo
from config.config import Config


def connect_to_mongodb():
    """Connects to MongoDB using the given MongoDB URI."""
    try:
        connection = pymongo.MongoClient(Config.DATABASE_URL)
        print("Connected to MongoDB")
        return connection
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB: {}".format(e))
        return None


if __name__ == "__main__":
    connection = connect_to_mongodb()
