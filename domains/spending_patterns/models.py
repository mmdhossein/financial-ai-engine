from sklearn.cluster import KMeans
import pandas as pd
from .repository import SpendingPatternsRepository
class SpendingPatternsModel:
    def __init__(self, n_clusters=3):
        self.model = KMeans(n_clusters=n_clusters)
        self.cluster_labels = None
        self.repository = SpendingPatternsRepository()

    def train(self, data: pd.DataFrame):
        self.cluster_labels = self.model.fit_predict(data[['amount']])
        print("done training")
        data['cluster'] = self.cluster_labels
        self.repository.save_cluster_assignments(data)



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
