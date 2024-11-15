import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import numpy as np
import pickle
from pymongo import MongoClient
from config.config import Settings
from services.redis import get_redis_service
import difflib
from tmdb.tmdb import fetch_movie_detail
import asyncio

# Global variables for cosine similarity, indices, and DataFrame
cosine_sim = None
indices = None
df = None
redis_service = get_redis_service()

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data_from_db():
    settings = Settings()
    client = MongoClient(settings.DATABASE_URL)
    db = client['pbl6']
    data_collection = db['content_based_data']
    data = list(data_collection.find().limit(5000))
    return pd.DataFrame(data)

# Initialize or load recommendation data
async def initiate_content_based_recommendation():
    global cosine_sim, indices, df
    try:
        cosine_sim = redis_service.get('cosine_sim')
        indices = redis_service.get('indices')

        # Load df directly from MongoDB instead of caching in Redis
        df = load_data_from_db()
        logger.info("Load data success")
        # If cosine_sim and indices exist in Redis, load them from cache
        if indices is not None:
            indices = pickle.loads(indices)
            print("Cache hit")
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(df['combined'])
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        else:
            # Create TF-IDF matrix with limited features to reduce memory usage
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(df['combined'])

            # Calculate cosine similarity matrix using sparse matrix format
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
            indices = pd.Series(df.index, index=df['title']).drop_duplicates()
            print("Cache miss")
            redis_service.set('indices', pickle.dumps(indices), 120)
            print("Cache indices")
        
        logger.info("Init recommender successful!")
    except Exception as e:
        logger.error(f"Error initializing content-based recommendation: {e}")

# Recommendation function for exact title match
async def get_recommendations(title):
    cached_recommendations = redis_service.get(f'recommendation:{title}')
    if cached_recommendations:
        return pickle.loads(cached_recommendations)

    if title not in indices:
        return {'error': 'Title not found'}
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:21]  # Exclude the movie itself
    movie_indices = [i[0] for i in sim_scores]
    
    recommendations = df.iloc[movie_indices]['id'].tolist()

    redis_service.set(f'recommendation:{title}', pickle.dumps(recommendations))
    result = await asyncio.gather(*(fetch_movie_detail(movie_id) for movie_id in recommendations))
    return result


# Fuzzy title matching
def get_closest_title(query):
    query = str(query)
    titles = df['title'].tolist()
    closest_matches = difflib.get_close_matches(query, titles, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

# Fuzzy recommendation function
async def get_recommendations_fuzzy(query):
    closest_title = get_closest_title(query)
    if closest_title:
        return await get_recommendations(closest_title)
    else:
        return {'error': 'No close match found'}
