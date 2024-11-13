import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import pickle
from pymongo import MongoClient
from config.config import Settings
from services.redis import get_redis_service

# Global variables for cosine similarity, indices, and DataFrame
cosine_sim = None
indices = None
df = None
redis_service = get_redis_service()

def load_data_from_db():
    settings = Settings()
    client = MongoClient(settings.DATABASE_URL)
    db = client['pbl6']
    data_collection = db['content_based_data']
    data = list(data_collection.find())
    return pd.DataFrame(data)

# Initialize or load recommendation data
async def initiate_content_based_recommendation():
    global cosine_sim, indices, df

    cosine_sim = redis_service.get('cosine_sim')
    indices = redis_service.get('indices')
    df = redis_service.get('df')

    #If the data exists in Redis, no need to recalculate
    if cosine_sim is not None and indices is not None and df is not None:
        cosine_sim = pickle.loads(cosine_sim)
        indices = pickle.loads(indices)
        df = pickle.loads(df)
        return

    df = load_data_from_db()

    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'])

    # Calculate cosine similarity matrix and indices
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    #Cache the computed data in Redis
    redis_service.set('cosine_sim', pickle.dumps(cosine_sim))
    redis_service.set('indices', pickle.dumps(indices))
    redis_service.set('df', pickle.dumps(df))
    
    print("Init recommender successful!")

# Recommendation function for exact title match
def get_recommendations(title):
    if title not in indices:
        return {'error': 'Title not found'}
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]  # Exclude the movie itself
    movie_indices = [i[0] for i in sim_scores]
    recommendations = df[['id', 'title']].iloc[movie_indices]
    return recommendations.to_json(orient='records')

# Fuzzy title matching
def get_closest_title(query):
    titles = df['title'].tolist()
    closest_matches = difflib.get_close_matches(query, titles, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

# Fuzzy recommendation function
async def get_recommendations_fuzzy(query):
    closest_title = get_closest_title(query)
    if closest_title:
        return get_recommendations(closest_title)
    else:
        return {'error': 'No close match found'}