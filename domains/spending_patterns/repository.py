# from pymongo import MongoClient

class SpendingPatternsRepository:
    def __init__(self):
        self.db  = {};
        # client = MongoClient("mongodb://localhost:27017/")
        # self.db = client['financial_ai']

    # def fetch_training_data(self):
        # return self.db['transactions'].find()
