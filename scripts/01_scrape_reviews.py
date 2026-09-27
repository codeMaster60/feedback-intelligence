from google_play_scraper import reviews, Sort
import pandas as pd

APP_IDS = {
    "swiggy": "in.swiggy.android",
    "phonepe": "com.phonepe.app",
}

all_reviews = []
for name, app_id in APP_IDS.items():
    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=800
    )
    for r in result:
        r['app'] = name
    all_reviews.extend(result)

df = pd.DataFrame(all_reviews)
df = df[['app', 'reviewId', 'content', 'score', 'at', 'thumbsUpCount']]
df.columns = ['app', 'review_id', 'text', 'rating', 'timestamp', 'helpful_count']
df.to_csv('data/raw_reviews.csv', index=False)
print(f"Saved {len(df)} reviews")

