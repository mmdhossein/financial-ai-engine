from flask import request, jsonify
from .services import SpendingPatternsService
from app.tests.synthetic_transactions import generate_transactions_with_segments,generate_daily_aggregates, generate_realistic_transactions
service = SpendingPatternsService()
import pandas as pd
from .repository import SpendingPatternsRepository
# Train the spending patterns model
def train():
    # repository = new SpendingPatternsRepository()
    # repository.deleteClusters()  
    for _ in range(0, 10):
        try:
            # Fetch and preprocess data from an external service
            # training_data = service.fetch_training_data()
            training_data_df = generate_realistic_transactions(1000)
            daily_aggregates = generate_daily_aggregates(training_data_df)
            #Deduplicate After Generation
            # transactions_df = transactions_df.drop_duplicates(subset=['userSerial'])
            # Check for duplicates
            # duplicates = training_data_df['userSerial'].duplicated().sum()
            # print(f"Number of duplicate user_serials: {duplicates}")

            # Ensure uniqueness
            # unique_user_serials = training_data_df['userSerial'].nunique()
            # total_user_serials = training_data_df['userSerial'].size
            # print(f"Unique user_serials: {unique_user_serials} / Total user_serials: {total_user_serials}")

            print("done fetching training data", training_data_df.head())
            processed_df = service.preprocess_data(training_data_df)
            print("processed_df", processed_df.head())
            clustered_data :pd.DataFrame= service.train_spending_pattern_model(processed_df)
            print("clustered_data", clustered_data.head())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Spending patterns model trained successfully!"
                    , "status": "successfully_trained"}), 200


# Get customer spending insights
def get_insights():
    try:
        # Example query parameters
        user_id = request.args.get('user_id')
        print("recieved user_id", user_id)
        insights = service.get_user_insights(user_id)
        return jsonify(insights), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
