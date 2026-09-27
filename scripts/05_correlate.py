import pandas as pd

reviews = pd.read_csv('data/clustered_reviews.csv', parse_dates=['timestamp'])
errors = pd.read_csv('data/synthetic_errors.csv', parse_dates=['date'])

correlations = []
for cid in sorted(reviews['cluster_id'].unique()):
    cluster_data = reviews[reviews['cluster_id'] == cid]
    feature = cluster_data['feature_area'].mode()[0]
    date_min, date_max = cluster_data['timestamp'].min(), cluster_data['timestamp'].max()

    window_errors = errors[
        (errors['feature_area'] == feature) &
        (errors['date'] >= date_min - pd.Timedelta(days=2)) &
        (errors['date'] <= date_max + pd.Timedelta(days=2))
    ]

    baseline = errors[errors['feature_area'] == feature]['affected_users_count'].median()
    peak = window_errors['affected_users_count'].max() if len(window_errors) else 0

    sample_text = cluster_data['text'].iloc[0][:60]

    correlations.append({
        'cluster_id': cid,
        'sample_text': sample_text,
        'feature_area': feature,
        'review_count': len(cluster_data),
        'error_spike_ratio': round(peak / baseline, 1) if baseline > 0 else 0
    })

result = pd.DataFrame(correlations).sort_values('error_spike_ratio', ascending=False)
result.to_csv('data/correlations.csv', index=False)
print(result.to_string(index=False))
