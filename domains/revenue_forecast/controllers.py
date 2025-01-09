from flask import request, jsonify
from .services import RevenueForecastService

service = RevenueForecastService()

# Train the revenue forecast model
def train():
    try:
        training_data = service.fetch_training_data()
        service.train_forecast_model(training_data)
        return jsonify({"message": "Revenue forecast model trained successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Predict future revenue
def predict():
    try:
        # Example query parameters
        time_horizon = request.args.get('time_horizon', 30)  # Default: next 30 days
        predictions = service.predict(time_horizon)
        return jsonify(predictions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
