from .models import SpendingPatternsModel
from .repository import SpendingPatternsRepository
import requests
import pandas as pd
import joblib
from flask import request, jsonify

class SpendingPatternsService:
    def __init__(self):
        self.repository = SpendingPatternsRepository()
        self.model = SpendingPatternsModel()

    def generate_patterns(self):
        # data = self.repository.fetch_training_data()
        # self.model.train(data)
        return self.model

    def fetch_data(self, api_url, params):
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            response.raise_for_status()

    def preprocess_data(self, df:pd.DataFrame):
        # Handle missing values
        df = df.dropna()
        # Normalize numeric columns
        df['amount'] = (df['amount'] - df['amount'].mean()) / df['amount'].std()
        # Encode categorical variables (e.g., transaction type)
        df = pd.get_dummies(df, columns=['transactionType'], drop_first=True)

        return df

    def train_spending_pattern_model(self, data):
        # model = KMeans(n_clusters=3)
        # model.fit(data[['amount']])
        self.model.train(data)
        return data



    def save_model(self, model, model_name):
        joblib.dump(model, f"{model_name}.joblib")

    def get_user_insights(self, user_id):
        # Fetch the user's cluster assignment
        user_data = self.repository.fetch_user_data(user_id)
        if user_data is None:
            return {"message": f"No data found for user_id: {user_id}"}
        
        cluster_id = user_data['cluster']
        cluster_details = self.repository.fetch_cluster_details(cluster_id)
        return {
            "user_id": user_id,
            "cluster_id": cluster_id,
            "cluster_details": cluster_details
        }

    def get_cluster_insights(self):
        # Summarize cluster details
        return self.repository.fetch_all_cluster_details()




# save_model(model, "spending_pattern_model")


# Example Usage
# api_url = "http://localhost:8080/transactions"
# params = {"startDate": "2023-01-01", "endDate": "2023-01-31", "partnerId": "123"}
# transactions_df = fetch_data(api_url, params)
# print(transactions_df.head())

# processed_df = preprocess_data(transactions_df)
# print(processed_df.head())

# model, clustered_data = train_spending_pattern_model(processed_df)
# print(clustered_data.head())
 
