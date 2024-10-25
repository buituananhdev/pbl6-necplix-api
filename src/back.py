import pandas as pd
import pandas as pd
from fastapi.responses import JSONResponse
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# Set up relative paths
base_path = Path(__file__).resolve().parent
movies_path = base_path / 'data' / 'movies.csv'
ratings_path = base_path / 'data' / 'ratings.csv'

ratings_df = pd.read_csv(ratings_path)
movie_df = pd.read_csv(movies_path)

user_id = 26

# Pivot DataFrame từ ratings_df
user_item_matrix = ratings_df.pivot_table(index='userId', columns='movieId', values='rating')

# Điền các giá trị NaN (chưa được đánh giá) bằng 0 hoặc giá trị trung bình
user_item_matrix = user_item_matrix.fillna(0)

# Tìm phim theo tiêu đề (ví dụ từ khóa "spider-man")
def search_movies_by_title(movie_df, search_query):
    search_query_lower = search_query.lower()
    return movie_df[movie_df['title'].str.lower().str.contains(search_query_lower)]

# Ví dụ tìm kiếm với từ khóa "spider-man"
searched_movies = search_movies_by_title(movie_df, 'spider-man')

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

# Ví dụ: Tìm người dùng tương tự và lấy phim từ họ
similar_users = get_similar_users(user_id, user_item_matrix, top_n=10)
recommended_movies_from_users = get_movies_from_similar_users(similar_users, user_item_matrix, movie_df)

# Tính độ tương đồng cosine giữa các bộ phim
movie_item_matrix = cosine_similarity(user_item_matrix.T)  # Chuyển vị ma trận user-item để có movie-item
movie_item_matrix = pd.DataFrame(movie_item_matrix, index=user_item_matrix.columns, columns=user_item_matrix.columns)


def get_similar_movies(movie_id, movie_item_matrix, top_n=10):
    # Lấy các giá trị độ tương đồng cho bộ phim đã tìm kiếm
    similar_scores = movie_item_matrix[movie_id]

    # Sắp xếp và lấy ra top N bộ phim tương tự
    similar_movies = similar_scores.sort_values(ascending=False).head(top_n)

    return similar_movies.index.tolist()

# Ví dụ: Tìm phim tương tự dựa trên phim đã tìm kiếm
for movie_id in searched_movies['movieId'].values:
    similar_movies = get_similar_movies(movie_id, movie_item_matrix, top_n=10)

def combine_recommendations(user_movies, similar_movies):
    # Chuyển đổi danh sách phim từ người dùng thành DataFrame
    user_movies_df = pd.DataFrame(user_movies, columns=['movieId'])

    # Chuyển đổi danh sách phim tương tự thành DataFrame
    similar_movies_df = pd.DataFrame(similar_movies, columns=['movieId'])

    # Kết hợp hai DataFrame
    combined_recommendations = pd.concat([user_movies_df, similar_movies_df]).drop_duplicates().reset_index(drop=True)

    return combined_recommendations


# Kết hợp các gợi ý
final_recommendations = combine_recommendations(recommended_movies_from_users, similar_movies)

# Lấy thông tin tiêu đề cho các phim gợi ý
final_recommendations = final_recommendations.merge(movie_df[['movieId', 'title']], on='movieId', how='left')

# Ưu tiên các phim tương tự nhất
def weighted_combination(user_similarities, item_similarities):
    return (user_similarities * 0.5) + (item_similarities * 0.5)  # Adjust weights as needed

def prioritize_search_results(recommendations, search_query):
    search_query_lower = search_query.lower()
    recommendations['score'] = recommendations['title'].apply(lambda x: x.lower().count(search_query_lower))
    recommendations = recommendations.sort_values(by='score', ascending=False)
    return recommendations

# Ưu tiên phim liên quan tới từ khóa tìm kiếm
final_recommendations = prioritize_search_results(final_recommendations, 'spider-man')





