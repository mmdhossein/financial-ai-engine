from .models import SpendingPatternsModel
from .repository import SpendingPatternsRepository
import requests
import pandas as pd
from sklearn.cluster import KMeans
import joblib

class SpendingPatternsService:
    def __init__(self):
        self.repository = SpendingPatternsRepository()
        self.model = SpendingPatternsModel()

    def generate_patterns(self):
        # data = self.repository.fetch_training_data()
        # self.model.train(data)
        return self.model

    def fetch_data(api_url, params):
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            response.raise_for_status()

    def preprocess_data(df):
        # Handle missing values
        df = df.dropna()

        # Normalize numeric columns
        df['amount'] = (df['amount'] - df['amount'].mean()) / df['amount'].std()

        # Encode categorical variables (e.g., transaction type)
        df = pd.get_dummies(df, columns=['transactionType'], drop_first=True)

        return df

    def train_spending_pattern_model(data):
        model = KMeans(n_clusters=3)
        model.fit(data[['amount']])
        data['cluster'] = model.labels_
        return model, data



    def save_model(model, model_name):
        joblib.dump(model, f"{model_name}.joblib")



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
 
