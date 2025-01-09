# from pymongo import MongoClient
from datetime import datetime

# def save_model_metadata(model_name, training_range):
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client['financial_ai']
#     metadata = {
#         "model_name": model_name,
#         "training_range": training_range,
#         "trained_at": datetime.now()
#     }
#     db['model_metadata'].insert_one(metadata)

# save_model_metadata("spending_pattern_model", {"start": "2023-01-01", "end": "2023-01-31"})
