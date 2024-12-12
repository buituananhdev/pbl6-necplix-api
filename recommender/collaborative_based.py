import pandas as pd
import numpy as np
import logging
import pickle
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from common.services.redis import get_redis_service
from common.services.database import load_data_from_db

# Initialize logging and Redis service
redis_service = get_redis_service()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Global settings
chunk_size = 100  # Number of columns (movies) per chunk
CACHE_EXPIRATION_TIME = 3600  # 1 hour

# Function to calculate cosine similarity in chunks
def calculate_and_cache_similarity_in_chunks(user_item_matrix, chunk_size=100):
    n_cols = user_item_matrix.shape[1]  # Number of movies
    for start in range(0, n_cols, chunk_size):
        end = min(start + chunk_size, n_cols)
        chunk_key = f"collaborative_cosine_sim_chunk:{start}:{end}"

        # Check if chunk exists in Redis
        cached_chunk = redis_service.get(chunk_key)
        if cached_chunk:
            logger.info(f"Loaded cosine similarity chunk from cache: {chunk_key}")
            continue

        # Calculate cosine similarity for the chunk
        logger.info(f"Calculating cosine similarity for chunk: {start}-{end}")
        chunk_matrix = user_item_matrix[:, start:end]
        cosine_sim_chunk = cosine_similarity(chunk_matrix.T)

        # Cache the result in Redis
        redis_service.set(chunk_key, pickle.dumps(cosine_sim_chunk), CACHE_EXPIRATION_TIME)
        logger.info(f"Cached cosine similarity chunk: {chunk_key}")

# Optimized initialization function
async def initiate_collaborative_based_recommendation():
    logger.info("Initializing collaborative-based recommendation...")
    try:
        # Load data from DB
        ratings_df = pd.DataFrame(load_data_from_db("collaborative_based_ratings", limit=80000))
        movies_df = pd.DataFrame(load_data_from_db("collaborative_based_movies", limit=1000000))
        logger.info("Data loaded successfully.")

        # Create user-item matrix (using sparse matrix for memory efficiency)
        user_item_matrix = ratings_df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
        user_item_matrix = csr_matrix(user_item_matrix.values)  # Convert to sparse matrix

        # Calculate and cache cosine similarity in chunks
        calculate_and_cache_similarity_in_chunks(user_item_matrix, chunk_size)

        logger.info("Collaborative-based recommendation initialized successfully.")
        return user_item_matrix, movies_df
    except Exception as e:
        print(e)
        logger.error(f"Error initializing collaborative-based recommendation: {e}")
        return None, None

# Function to retrieve similarity chunk
def get_similarity_chunk(start, end):
    chunk_key = f"collaborative_cosine_sim_chunk:{start}:{end}"
    cached_chunk = redis_service.get(chunk_key)
    if cached_chunk:
        return pickle.loads(cached_chunk)
    return None
