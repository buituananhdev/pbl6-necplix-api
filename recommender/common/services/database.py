from pymongo import MongoClient
from common.config.config import Settings

def load_data_from_db(collection_name, limit=None, fields=None):
    """
    Load data from MongoDB and return as a pandas DataFrame.

    :param collection_name: Name of the MongoDB collection to query.
    :param limit: Maximum number of documents to fetch. If None, fetch all documents.
    :param fields: List of fields to include in the result. If None, fetch all fields.
    :return: A pandas DataFrame containing the data, or None if an error occurs.
    """
    try:
        settings = Settings()
        client = MongoClient(settings.DATABASE_URL)
        db = client['pbl6']
        data_collection = db[collection_name]
        
        # Build the projection for fields (None means fetch all fields)
        projection = {field: 1 for field in fields} if fields else None
        
        # Fetch data with optional limit and projection
        cursor = data_collection.find({}, projection)
        if limit:
            cursor = cursor.limit(limit)
        
        data = list(cursor)
        return data
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return None
