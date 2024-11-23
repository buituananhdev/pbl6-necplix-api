import pandas as pd
import numpy as np
import logging
import json
import difflib
from common.services.redis import get_redis_service
from common.services.database import load_data_from_db
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Initialize logging and Redis service
redis_service = get_redis_service()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Cache expiration time (in seconds)
CACHE_EXPIRATION_TIME = 3600  # 1 hour

# Chunk size
chunk_size = 5000  # Number of rows per chunk

# Optimized initialization function
async def initiate_collaborative_based_recommendation():
    logger.info("Initializing collaborative-based recommendation...")
    try:
        # Load data from DB
        ratings_df = load_data_from_db("collaborative_based_ratings", limit=80000)
        movies_df = load_data_from_db("collaborative_based_movies", limit=1000000)

        # Create user-item matrix (using sparse matrix for memory efficiency)
        user_item_matrix = ratings_df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        user_item_matrix = csr_matrix(user_item_matrix.values)  # Convert to sparse matrix

        # Calculate and cache movie similarity for all movies once during initialization
        movie_similarities = cosine_similarity(user_item_matrix.T)
        redis_service.set("movie_similarities", pickle.dumps(movie_similarities))
        logger.info("Precomputed movie similarities and cached them.")

        logger.info("Collaborative-based recommendation initialized successfully.")
        return user_item_matrix, movies_df
    except Exception as e:
        logger.error(f"Error initializing collaborative-based recommendation: {e}")
        return None, None
