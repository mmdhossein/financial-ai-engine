import random
import pandas as pd
from datetime import datetime, timedelta
import uuid
# V1 Generate synthetic transactions with customer segments
def generate_transactions_with_segments(num_records):
    data = []
    
    # Define customer segments
    segments = {
        "High Spenders": {"probability": 0.2, "spend_range": (500, 1000), "frequency": (1, 3)},
        "Occasional Buyers": {"probability": 0.6, "spend_range": (50, 200), "frequency": (3, 7)},
        "Budget-Conscious": {"probability": 0.2, "spend_range": (10, 50), "frequency": (5, 10)},
    }
    
    for _ in range(num_records):
        # Select a segment based on probability
        segment = random.choices(
            list(segments.keys()), 
            weights=[segments[s]["probability"] for s in segments], 
            k=1
        )[0]
        
        # Generate data based on segment characteristics
        user_serial = f"user_{random.randint(1, 9999999999)}"
        # user_serial = f"user_{uuid.uuid4().hex}"
        partner_id = f"partner_{random.randint(1, 50)}"
        transaction_type = random.choice(["purchase", "refund", "subscription"])
        amount = round(random.uniform(*segments[segment]["spend_range"]), 2)
        transaction_count = random.randint(*segments[segment]["frequency"])
        
        # Create multiple transactions for the same user
        for _ in range(transaction_count):
            time = datetime.now() - timedelta(days=random.randint(0, 365))
            data.append({
                "userSerial": user_serial,
                "partnerId": partner_id,
                "transactionType": transaction_type,
                "amount": amount,
                "time": time,
                "segment": segment  # Add segment label
            })
    
    return pd.DataFrame(data)

# Generate daily aggregates
def generate_daily_aggregates(transactions):
    transactions['actionDate'] = transactions['time'].dt.date
    aggregates = transactions.groupby(['actionDate', 'partnerId', 'transactionType']).agg(
        totalAmount=('amount', 'sum'),
        counts=('amount', 'count')
    ).reset_index()
    return aggregates

# Generate data
# transactions = generate_transactions_with_segments(1000)
# daily_aggregates = generate_daily_aggregates(transactions)

# Save to CSV
# transactions.to_csv("synthetic_transactions_with_segments.csv", index=False)
# daily_aggregates.to_csv("synthetic_daily_aggregates.csv", index=False)

# Preview data
# print("Transactions Sample:")
# print(transactions.head())
# print("\nDaily Aggregates Sample:")
# print(daily_aggregates.head())  

# V2 To mimic more realistic scenario of users
def generate_user_behavior(user_serial, num_periods=3):
    data = []
    for _ in range(num_periods):
        partner_id = f"partner_{random.randint(1, 50)}"
        transaction_type = random.choice(["purchase", "subscription", "refund", "charge"])
        amount = round(random.uniform(50, 1000), 2)
        time = datetime.now() - timedelta(days=random.randint(0, 365))

        # Simulate changes in behavior
        if time.month in [11, 12]:  # Higher spending in November/December
            amount *= 1.5
        elif transaction_type == "refund":  # Lower amounts for refunds
            amount *= 0.5

        data.append({
            "userSerial": user_serial,
            "partnerId": partner_id,
            "transactionType": transaction_type,
            "amount": amount,
            "time": time
        })
    return data

# Generate realistic data for multiple users
def generate_realistic_transactions(num_users=1000):
    all_data = []
    for user_id in range(1, num_users + 1):
        user_serial = f"user_{user_id}"
        user_data = generate_user_behavior(user_serial, num_periods=random.randint(1, 30))
        all_data.extend(user_data)
    return pd.DataFrame(all_data)