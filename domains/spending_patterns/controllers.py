from flask import request, jsonify
from .services import SpendingPatternsService
from app.tests.synthetic_transactions import generate_transactions_with_segments, generate_daily_aggregates
service = SpendingPatternsService()
import pandas as pd
# Train the spending patterns model
def train():
    try:
        # Fetch and preprocess data from an external service
        # training_data = service.fetch_training_data()
        training_data_df = generate_transactions_with_segments(1000)
        daily_aggregates = generate_daily_aggregates(training_data_df)
        print("done fetching training data", training_data_df.head())
        processed_df = service.preprocess_data(training_data_df)
        print("processed_df", processed_df.head())
        clustered_data :pd.DataFrame= service.train_spending_pattern_model(processed_df)
        print("clustered_data", clustered_data.head())
        return jsonify({"message": "Spending patterns model trained successfully!"
                        ,"data": clustered_data.head().to_dict(), "status": "successfully_trained"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get customer spending insights
def get_insights():
    try:
        # Example query parameters
        user_id = request.args.get('user_id')
        insights = service.get_user_insights(user_id)
        return jsonify(insights), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
