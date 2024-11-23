import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from common.services.redis import get_redis_service
import logging
from common.services.database import load_data_from_db
from rapidfuzz import process

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
redis_service = get_redis_service()
chunk_size = 500  # Number of rows per chunk
df = None

# Helper function to calculate TF-IDF and cosine similarity in chunks
async def load_tfidf_matrix_in_chunks(df, chunk_size=500):
    tfidf = TfidfVectorizer(stop_words='english')
    num_rows = len(df)
    
    for start in range(0, num_rows, chunk_size):
        end = min(start + chunk_size, num_rows)
        chunk_key = f"content_cosine_sim_chunk:{start}:{end}"

        # Check if the chunk is already in Redis
        cached_chunk = redis_service.get(chunk_key)
        if cached_chunk:
            logger.info(f"Loaded cosine similarity chunk from cache: {chunk_key}")
            continue  # Skip recalculating if chunk is already cached

        # If not found in Redis, calculate and store it
        tfidf_matrix_chunk = tfidf.fit_transform(df['combined'].iloc[start:end])
        cosine_sim_chunk = cosine_similarity(tfidf_matrix_chunk, tfidf_matrix_chunk)

        # Store the calculated chunk in Redis with a reasonable expiration time
        redis_service.set(chunk_key, pickle.dumps(cosine_sim_chunk), ttl=36000)  # Cache expires in 10 hours
        logger.info(f"Cached cosine similarity chunk: {chunk_key}")


# Get chunk key for a given index
def get_chunk_for_index(idx, chunk_size=500):
    start = (idx // chunk_size) * chunk_size
    end = start + chunk_size
    return f"content_cosine_sim_chunk:{start}:{end}"

# Initialize or load recommendation data
async def initiate_content_based_recommendation_optimized():
    logger.info("Initializing content-based recommendation with optimization...")
    global df
    try:
        # Load data from database (assuming load_data_from_db loads data from MongoDB or other source)
        df = pd.DataFrame(load_data_from_db("content_based_data", limit=45000))
        logger.info("Data loaded successfully")

        # Calculate and cache cosine similarity in chunks
        await load_tfidf_matrix_in_chunks(df, chunk_size)
        logger.info("Content-based recommendation initialization completed!")
    except Exception as e:
        logger.error(f"Error initializing content-based recommendation: {e}")

# Recommendation function for exact title match
async def get_recommendations(title):
    logger.info(f"Getting recommendations for: {title}")
    cached_recommendations = redis_service.get(f'recommendation:{title}')
    if cached_recommendations:
        return pickle.loads(cached_recommendations)

    idx = df.index[df['title'] == title].tolist()
    if not idx:
        return {'error': 'Title not found'}

    idx = idx[0]
    chunk_key = get_chunk_for_index(idx)
    cosine_sim_chunk = pickle.loads(redis_service.get(chunk_key))

    sim_scores = list(enumerate(cosine_sim_chunk[idx % chunk_size]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:21]  # Top 20 similar movies
    movie_indices = [i[0] for i in sim_scores]

    recommendations = df.iloc[movie_indices]['id'].tolist()
    redis_service.set(f'recommendation:{title}', pickle.dumps(recommendations), ttl=600)  # Cache expiration time 10 minutes
    return recommendations

# Fuzzy title matching function
def get_closest_title(query):
    titles = load_data_from_db("content_based_data", fields=["title"])
    titles = [movie["title"] for movie in titles]
    closest_match = process.extractOne(query, titles, score_cutoff=60)
    return closest_match[0] if closest_match else None

# Fuzzy recommendation function
async def get_recommendations_fuzzy(query):
    closest_title = get_closest_title(query)
    if closest_title:
        return await get_recommendations(closest_title)
    else:
        return {'error': 'No close match found'}
