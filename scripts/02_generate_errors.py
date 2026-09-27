import pandas as pd
import numpy as np

reviews_df = pd.read_csv('data/raw_reviews.csv', parse_dates=['timestamp'])
review_max = reviews_df['timestamp'].max()

# Use a fixed 60-day window ending at the last review date
date_max = review_max.normalize()
date_min = date_max - pd.Timedelta(days=59)

feature_areas = ['payment_gateway', 'order_tracking', 'search', 'login_auth', 'checkout', 'notifications']
error_types = ['timeout', 'crash', '500_error', 'latency_spike']

rows = []
date_range = pd.date_range(date_min, date_max, freq='D')

for date in date_range:
    for feature in feature_areas:
        baseline = np.random.poisson(2)
        rows.append([date, feature, np.random.choice(error_types), baseline])

# Inject spikes, including at least one inside the review window (last 2 days)
spike_dates = list(pd.to_datetime(np.random.choice(date_range[:-2], 3, replace=False)))
spike_dates.append(date_max)  # guarantee a spike on the last day, inside review range
spike_dates.append(date_max - pd.Timedelta(days=1))

for date in spike_dates:
    feature = np.random.choice(feature_areas)
    rows.append([date, feature, '500_error', np.random.randint(150, 400)])
    print(f"Injected spike: {feature} on {date.date()}")

df = pd.DataFrame(rows, columns=['date', 'feature_area', 'error_type', 'affected_users_count'])
df.to_csv('data/synthetic_errors.csv', index=False)
print(f"Saved {len(df)} error rows across {len(date_range)} days")
