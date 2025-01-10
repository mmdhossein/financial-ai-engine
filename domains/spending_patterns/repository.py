import pandas as pd
from datetime import datetime, date

class SpendingPatternsRepository:
    def __init__(self):
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client['financial_ai']

    def fetch_training_data(self):
        # Fetch transactions data from the database
        return pd.DataFrame(list(self.db['transactions'].find()))

    def save_cluster_assignments(self, data: pd.DataFrame):
        # Save the cluster assignments back to the database
        for column in data.select_dtypes(include=['object', 'datetime']).columns:
            data[column] = data[column].apply(
                lambda x: datetime.combine(x, datetime.min.time()) if isinstance(x, date) else x
            )
        # self.db['clusters'].delete_many({})  # Clear old assignments
        print("sexy", data.to_dict('records')[2])
        self.db['clusters'].insert_many(data.to_dict('records'))

    def deleteClusters(self):
        self.db['clusters'].delete_many({})  # Clear old assignments


    def fetch_user_data(self, user_id):
        # Fetch user data and their cluster assignment
        return self.db['clusters'].find({"userSerial": user_id})

    def fetch_cluster_details(self, cluster_id):
        # Fetch aggregated details for a specific cluster
        return self.db['clusters'].aggregate([
            {"$match": {"cluster": cluster_id}},
            {"$group": {
                "_id": "$cluster",
                "average_spending": {"$avg": "$amount"},
                "user_count": {"$sum": 1}
            }}, 
            {"$project":  {'_id': 0}
            }
        ])

    def fetch_all_cluster_details(self):
        # Fetch summaries for all clusters
        return list(self.db['clusters'].aggregate([
            {"$group": {
                "_id": "$cluster",
                "average_spending": {"$avg": "$amount"},
                "user_count": {"$sum": 1}
            }}
        ]))
