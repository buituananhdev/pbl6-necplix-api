import pandas as pd
from pymongo import MongoClient
from common.config.config import Settings

def load_data_from_db(collection_name, limit=50):
    try:
        settings = Settings()
        client = MongoClient(settings.DATABASE_URL)
        db = client['pbl6']
        data_collection = db[collection_name]
        data = list(data_collection.find().limit(limit))
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return None