from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.utils import logger
from app.utils.config import loadEnv

logger = logger.getLogger() 
MONGODB_USERNAME = loadEnv().get('MONGODB_USERNAME')
MONGODB_PASSWORD = loadEnv().get('MONGODB_PASSWORD')
MONGODB_URL = loadEnv().get('MONGODB_URL')
MONGODB_DB_NAME = loadEnv().get('MONGODB_DB_NAME')


def connect():
    uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_URL}/?retryWrites=true&w=majority&appName=cinema-plot"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Failed to connect to MongoDB")
        
    db = client[MONGODB_DB_NAME]
    
    return db

def get_collection(collection_name):
    db = connect()
    
    return db[collection_name]