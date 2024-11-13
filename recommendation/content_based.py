import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient
from config.config import Settings
from services.redis import get_redis_service
import pickle
# Global variables for cosine similarity and DataFrame
cosine_sim = None
indices = None
df2 = None
redis_service = get_redis_service()

nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    text = re.sub(r'\W', ' ', text).lower().strip()
    words = [word for word in text.split() if word not in set(stopwords.words('english'))]
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in words])

async def initiate_content_based_recommendation():
    global cosine_sim, indices, df2
    cosine_sim = redis_service.get('cosine_sim')
    indices = redis_service.get('indices')

    # Nếu cosine_sim và indices đã có trong Redis, chỉ cần trả về mà không tính lại
    if cosine_sim is not None and indices is not None:
        cosine_sim = pickle.loads(cosine_sim)
        indices = pickle.loads(indices)
        return
    
    settings = Settings()
    client = MongoClient(settings.DATABASE_URL)
    db = client['pbl6-db']
    credits_collection = db['tmdb_5000_credits']
    movies_collection = db['tmdb_5000_movies']

    # Load data from MongoDB
    credits_data = list(credits_collection.find())
    movies_data = list(movies_collection.find())

    # Convert data from MongoDB to DataFrame
    df1 = pd.DataFrame(credits_data)
    df2 = pd.DataFrame(movies_data)

    # Remove '_id' column if it exists
    df1 = df1.drop(columns=['_id'], errors='ignore')
    df2 = df2.drop(columns=['_id'], errors='ignore')

    # Process data
    df1.columns = ['id', 'title', 'cast', 'crew']
    df2 = df2.drop(columns=['title'])
    df2 = df2.merge(df1, on='id')
    df2 = df2.dropna(subset=['title'])
    df2['overview'] = df2['overview'].fillna('').apply(preprocess_text)
    df2['genres'] = df2['genres'].fillna('').apply(lambda x: ' '.join([i['name'] for i in x] if isinstance(x, list) else ''))
    df2['keywords'] = df2['keywords'].fillna('').apply(lambda x: ' '.join([i['name'] for i in x] if isinstance(x, list) else ''))
    df2['combined'] = df2['overview'] + ' ' + df2['genres'] + ' ' + df2['keywords']

    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df2['combined'])

    # Calculate cosine similarity matrix and indices
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()
    redis_service.set('cosine_sim', pickle.dumps(cosine_sim))
    redis_service.set('indices', pickle.dumps(indices))

# Recommendation function
def get_recommendations(title):
    if title not in indices:
        return {'error': 'Title not found'}
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]
    movie_indices = [i[0] for i in sim_scores]
    recommendations = df2[['id', 'title']].iloc[movie_indices]
    return recommendations.to_json(orient='records')

# Fuzzy title matching
def get_closest_title(query):
    titles = df2['title'].tolist()
    closest_matches = difflib.get_close_matches(query, titles, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

# Fuzzy recommendation function
async def get_recommendations_fuzzy(query):
    closest_title = get_closest_title(query)
    if closest_title:
        return get_recommendations(closest_title)
    else:
        return {'error': 'No close match found'}

# Example usage:
# await initiate_content_based_recommendation()
# recommendations = await get_recommendations_fuzzy("Movie Title")
