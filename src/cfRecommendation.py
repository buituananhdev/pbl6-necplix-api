import pandas as pd
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Set up relative paths
base_path = Path(__file__).resolve().parent
movies_path = base_path / 'data' / 'cf_movies.csv'
ratings_path = base_path / 'data' / 'cf_ratings.csv'

# Load data
ratings_df = pd.read_csv(ratings_path)
movie_df = pd.read_csv(movies_path)

# Pivot DataFrame từ ratings_df
user_item_matrix = ratings_df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# Tính độ tương đồng cosine giữa các bộ phim
movie_item_matrix = cosine_similarity(user_item_matrix.T)  # Chuyển vị ma trận user-item để có movie-item
movie_item_matrix = pd.DataFrame(movie_item_matrix, index=user_item_matrix.columns, columns=user_item_matrix.columns)

# Tạo hàm tính độ tương đồng giữa người dùng
def get_similar_users(user_id, ratings_matrix, top_n=10):
    user_ratings = ratings_matrix.loc[user_id].values.reshape(1, -1)
    user_similarities = cosine_similarity(ratings_matrix, user_ratings).flatten()
    similar_users_indices = user_similarities.argsort()[-top_n-1:-1][::-1]
    return ratings_matrix.index[similar_users_indices]

# Lấy danh sách phim yêu thích của người dùng tương tự
def get_movies_from_similar_users(similar_users, ratings_matrix, movie_df):
    movie_ids = ratings_matrix.loc[similar_users].mean().sort_values(ascending=False).index
    return movie_df[movie_df['movieId'].isin(movie_ids)]

# Lấy gợi ý phim cho người dùng
def get_CF_recommendations(user_id):
    if user_id not in user_item_matrix.index:
        return JSONResponse(content={'error': 'User ID not found'}, status_code=404)

    similar_users = get_similar_users(user_id, user_item_matrix, top_n=10)
    recommended_movies_from_users = get_movies_from_similar_users(similar_users, user_item_matrix, movie_df)

    return recommended_movies_from_users[['movieId', 'title']].to_dict('records')

# Hàm để ưu tiên các phim dựa trên từ khóa tìm kiếm
def prioritize_search_results(recommendations, search_query):
    search_query_lower = search_query.lower()
    recommendations['score'] = recommendations['title'].apply(lambda x: x.lower().count(search_query_lower))
    recommendations = recommendations.sort_values(by='score', ascending=False)
    return recommendations

# Ví dụ: Ưu tiên phim liên quan tới từ khóa tìm kiếm
def get_prioritized_recommendations(user_id, search_query):
    recommendations = get_CF_recommendations(user_id)
    recommendations_df = pd.DataFrame(recommendations)
    prioritized_recommendations = prioritize_search_results(recommendations_df, search_query)
    return prioritized_recommendations.to_dict('records')
