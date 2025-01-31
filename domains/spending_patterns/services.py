from .models import SpendingPatternsModel
from .repository import SpendingPatternsRepository
import requests
import pandas as pd
import joblib
from flask import request, jsonify
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt




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
        df['original_amount'] = df['amount']
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
        user_data_df = pd.DataFrame(list(user_data))
        print("user df", user_data_df.head())
        if user_data is None:
            return {"message": f"No data found for user_id: {user_id}"}
        # Calculate cluster likelihood
        # cluster_likelihood = (
        #     user_data_df.groupby(["userSerial", "cluster"])
        #     .size()
        #     .reset_index(name="count")
        #     .sort_values(by=["userSerial", "count"], ascending=False)
        # )

       
 
        cluster_likelihood = (
        user_data_df.groupby(["cluster"])
        .size()
        .reset_index(name="count")
        .sort_values(by=["count"], ascending=False)
        )
        
        # Add a recency weight (e.g., inverse of days since the transaction)
        user_data_df["days_ago"] = (datetime.now() - user_data_df["time"]).dt.days
        user_data_df["recency_weight"] = 1 / (user_data_df["days_ago"] + 1)  # Add 1 to avoid division by zero

        weighted_likelihood  = (
        user_data_df.groupby([ "cluster"])["recency_weight"]
        .sum()
        .reset_index()
        .sort_values(by=["recency_weight"], ascending=False)
        )

        print("calculated cluster_likelihood: ", cluster_likelihood.head())
        print("calculated weighted_likelihood: ", weighted_likelihood.head())


        # Merge counts and recency weights
        final_likelihood = pd.merge(
        cluster_likelihood,
        weighted_likelihood,
        on=["cluster"],
        how="left"
        )

        print("calculated final_likelihood: ", final_likelihood.head())


        # Combine scores (adjust weights as needed)
        final_likelihood["final_score"] = final_likelihood["count"] + final_likelihood["recency_weight"]

        # Get the top cluster for each user
        idxMax = final_likelihood["final_score"].idxmax()

        # cluster_id = user_data['cluster']
        cluster_id = (final_likelihood['cluster'].iloc[idxMax]).item()
        print("getting cluster info for cluster id: ", cluster_id )
        cluster_details = self.repository.fetch_cluster_details(cluster_id).to_list()
        return {
            "user_id": user_id,
            "cluster_id": cluster_id,
            "cluster_details": cluster_details
        }
    

    def get_cluster_insights(self):
        # Summarize cluster details
        return self.repository.fetch_all_cluster_details()
    
    def getModelMetrics(self):
        return self.model.getModelMetrics()
    
    def plotModelMetrics(eslf, metrics):
        df = pd.DataFrame(metrics)

        # Plot Inertia
        plt.figure(figsize=(10, 5))
        plt.plot(df["iteration"], df["inertia"], marker="o", label="Inertia")
        plt.title("Inertia Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Inertia")
        plt.legend()
        plt.show()

        # Plot Silhouette Score
        plt.figure(figsize=(10, 5))
        plt.plot(df["iteration"], df["silhouette_score"], marker="o", label="Silhouette Score")
        plt.title("Silhouette Score Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Silhouette Score")
        plt.legend()
        plt.show()




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
 
