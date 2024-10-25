import pandas as pd
from fastapi.responses import JSONResponse
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pathlib import Path

from .preprocessing import preprocess_text

# Load data
# Set up relative paths
base_path = Path(__file__).resolve().parent
movies_path = base_path / 'data' / 'movies.csv'
credits_path = base_path / 'data' / 'credits.csv'
df1 = pd.read_csv(credits_path)
df2 = pd.read_csv(movies_path)

df1.columns = ['id', 'tittle', 'cast', 'crew']
df2 = df2.merge(df1, on='id')
df2 = df2.dropna(subset=['title'])

# Preprocessing
df2['overview'] = df2['overview'].fillna('').apply(preprocess_text)
df2['genres'] = df2['genres'].fillna('').apply(lambda x: ' '.join([i['name'] for i in eval(x)]))
df2['keywords'] = df2['keywords'].fillna('').apply(lambda x: ' '.join([i['name'] for i in eval(x)]))

df2['combined'] = df2['overview'] + ' ' + df2['genres'] + ' ' + df2['keywords']

# TF-IDF and cosine similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df2['combined'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim):
    if title not in indices:
        return JSONResponse(content={'error': 'Title not found'}, status_code=404)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]
    movie_indices = [i[0] for i in sim_scores]

    recommendations = df2[['id', 'title']].iloc[movie_indices]

    return recommendations.to_dict('records')


def get_closest_title(query, titles):
    closest_match = process.extractOne(query, titles)
    return closest_match[0] if closest_match else None


def get_recommendations_fuzzy(query, cosine_sim=cosine_sim):
    closest_title = get_closest_title(query, df2['title'].tolist())
    if closest_title:
        return get_recommendations(closest_title, cosine_sim)
    else:
        return JSONResponse(content={'error': 'No close match found'}, status_code=404)
