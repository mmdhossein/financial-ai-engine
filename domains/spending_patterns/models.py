from sklearn.cluster import KMeans
import pandas as pd

class SpendingPatternsModel:
    def __init__(self, n_clusters=3):
        self.model = KMeans(n_clusters=n_clusters)

    def train(self, data: pd.DataFrame):
        return self.model.fit(data)

    def predict(self, data: pd.DataFrame):
        return self.model.predict(data)
