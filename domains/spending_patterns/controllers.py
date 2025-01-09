from flask import request, jsonify
from .services import SpendingPatternsService

service = SpendingPatternsService()

# Train the spending patterns model
# def train():
#     try:
#         # Fetch and preprocess data from an external service
#         training_data = service.fetch_training_data()
#         service.train_model(training_data)
#         return jsonify({"message": "Spending patterns model trained successfully!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# Get customer spending insights
def get_insights():
    try:
        # Example query parameters
        user_id = request.args.get('user_id')
        insights = service.get_insights(user_id)
        return jsonify(insights), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
