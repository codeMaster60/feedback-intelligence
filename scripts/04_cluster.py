import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

df = pd.read_csv('data/classified_reviews.csv')
actionable = df[df['category'].isin(['bug', 'feature_request', 'ux_confusion'])].copy()

print(f"Actionable reviews to cluster: {len(actionable)}")

vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1,2))
X = vectorizer.fit_transform(actionable['text'].astype(str))

n_clusters = max(5, min(25, len(actionable) // 10))
km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
actionable['cluster_id'] = km.fit_predict(X)

actionable.to_csv('data/clustered_reviews.csv', index=False)
print(f"Saved {len(actionable)} rows into {n_clusters} clusters")
print(actionable['cluster_id'].value_counts())
