import pandas as pd
from pymongo import MongoClient

client = MongoClient("")
db = client["pbl6"]
collection = db["content_based_data"]

file_path = r"C:\Users\Lenovo\Downloads\processed_data (3).csv"
data = pd.read_csv(file_path)

data_dict = data.to_dict(orient="records")

collection.insert_many(data_dict)

print("Dữ liệu đã được lưu vào MongoDB thành công!")
