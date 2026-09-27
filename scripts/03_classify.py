import pandas as pd
from groq import Groq
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

df = pd.read_csv('data/raw_reviews.csv')

# Resume support: skip rows already classified
already_done = set()
if os.path.exists('data/classified_reviews.csv'):
    prev = pd.read_csv('data/classified_reviews.csv')
    already_done = set(prev['review_id'])
    print(f"Resuming: {len(already_done)} rows already classified")

SYSTEM_PROMPT = """You are a product feedback classifier. Given a user review, respond with ONLY valid JSON, no markdown, no explanation:
{
  "category": "bug" | "feature_request" | "ux_confusion" | "duplicate_generic" | "noise",
  "feature_area": "payment_gateway" | "order_tracking" | "search" | "login_auth" | "checkout" | "notifications" | "other",
  "severity": 1-5,
  "sentiment": "positive" | "neutral" | "negative"
}
Classify "noise" for reviews with no actionable content (e.g. "good app", "nice")."""

results = []
for i, row in df.iterrows():
    if row['review_id'] in already_done:
        continue

    success = False
    attempts = 0
    while not success and attempts < 3:
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Review (rating {row['rating']}/5): {row['text']}"}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            parsed = json.loads(completion.choices[0].message.content)
            parsed['review_id'] = row['review_id']
            results.append(parsed)
            success = True
        except Exception as e:
            error_str = str(e)
            if 'rate_limit' in error_str or '429' in error_str:
                print(f"Rate limited on row {i}, waiting 20s...")
                time.sleep(20)
                attempts += 1
            else:
                print(f"Failed on row {i}: {e}")
                break

    if i % 20 == 0:
        print(f"Processed {i}/{len(df)}")

    # Save progress every 50 rows so we never lose work
    if len(results) % 50 == 0 and len(results) > 0:
        temp_class = pd.DataFrame(results)
        temp_merged = df.merge(temp_class, on='review_id')
        if os.path.exists('data/classified_reviews.csv'):
            existing = pd.read_csv('data/classified_reviews.csv')
            temp_merged = pd.concat([existing, temp_merged]).drop_duplicates(subset='review_id')
        temp_merged.to_csv('data/classified_reviews.csv', index=False)

    time.sleep(1.2)  # ~50 requests/minute, safely under token limits

# Final save
if results:
    class_df = pd.DataFrame(results)
    merged = df.merge(class_df, on='review_id')
    if os.path.exists('data/classified_reviews.csv'):
        existing = pd.read_csv('data/classified_reviews.csv')
        merged = pd.concat([existing, merged]).drop_duplicates(subset='review_id')
    merged.to_csv('data/classified_reviews.csv', index=False)

final = pd.read_csv('data/classified_reviews.csv')
print(f"Total classified: {len(final)} reviews")
