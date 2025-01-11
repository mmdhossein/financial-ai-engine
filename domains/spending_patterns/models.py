from sklearn.cluster import KMeans
import pandas as pd
from .repository import SpendingPatternsRepository
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
import numpy as np

class SpendingPatternsModel:
    def __init__(self, n_clusters=3):
        # self.model = KMeans(n_clusters=n_clusters)
        self.model = MiniBatchKMeans(n_clusters=3, random_state=42)# better for iterations batch_size=100
        self.cluster_labels = None
        self.repository = SpendingPatternsRepository()
        self.cluster_metrics = []

    def train(self, data: pd.DataFrame):
        # self.cluster_labels = self.model.fit_predict(data[['amount']])
        self.model.partial_fit(data[['amount']]) #Scalable for Streaming Data:
        self.cluster_labels = self.model.predict(data[['amount']])
        print("done training")
        # print("cluster_labels:", self.cluster_labels)
        data['cluster'] = self.cluster_labels
        self.repository.save_cluster_assignments(data)
        print("done saving assignments")
        print("calculating metrics...")
        self.evaluate_clustering(data[['amount']])



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
    
    def evaluate_clustering(self, data):
        # Inertia
        inertia = self.model.inertia_

        # Silhouette Score
        if len(set(self.cluster_labels)) > 1:  # Silhouette score requires at least 2 clusters
            silhouette = silhouette_score(data, self.cluster_labels)
        else:
            silhouette = np.nan  # Not applicable for 1 cluster

        print(f"Inertia: {inertia}")
        print(f"Silhouette Score: {silhouette}")

        metrics = {
        "inertia": inertia,
        "silhouette_score": silhouette,
        "n_clusters": len(set(self.cluster_labels)),
        "iteration": len(self.cluster_metrics) + 1  # Track iterations
        }

        self.cluster_metrics.append(metrics)

        return inertia, silhouette
    

    def getModelMetrics(self):
        return self.cluster_metrics



