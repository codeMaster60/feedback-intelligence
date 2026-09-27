import pandas as pd

reviews = pd.read_csv('data/clustered_reviews.csv')
corr = pd.read_csv('data/correlations.csv')

agg = reviews.groupby('cluster_id').agg(
    frequency=('review_id', 'count'),
    avg_severity=('severity', 'mean'),
    negative_ratio=('sentiment', lambda x: (x == 'negative').mean())
).reset_index()

merged = agg.merge(corr, on='cluster_id')

def normalize(col):
    return (col - col.min()) / (col.max() - col.min() + 1e-9)

merged['freq_norm'] = normalize(merged['frequency'])
merged['severity_norm'] = normalize(merged['avg_severity'])
merged['error_norm'] = normalize(merged['error_spike_ratio'])
merged['confidence_norm'] = normalize(merged['negative_ratio'])

merged['priority_score'] = (
    0.4 * merged['freq_norm'] +
    0.3 * merged['error_norm'] +
    0.2 * merged['severity_norm'] +
    0.1 * merged['confidence_norm']
)

ranked = merged.sort_values('priority_score', ascending=False)
ranked.to_csv('outputs/ranked_issues.csv', index=False)
print(ranked[['cluster_id', 'sample_text', 'feature_area', 'frequency', 'error_spike_ratio', 'priority_score']].to_string(index=False))
