import schedule
import time

def run_training_pipeline():
    # Fetch, preprocess, train, and save steps
    print("Running training pipeline...")

schedule.every().day.at("02:00").do(run_training_pipeline)

while True:
    schedule.run_pending()
    time.sleep(1)
