import pandas as pd
from groq import Groq
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

ranked = pd.read_csv('outputs/ranked_issues.csv')
reviews = pd.read_csv('data/clustered_reviews.csv')

os.makedirs('outputs/reports', exist_ok=True)
top_issues = ranked.head(5)

for _, issue in top_issues.iterrows():
    cluster_reviews = reviews[reviews['cluster_id'] == issue['cluster_id']]
    sample_quotes = cluster_reviews['text'].astype(str).head(3).tolist()

    prompt = f"""Write a developer-ready bug/issue report in markdown for this cluster:
Title: {issue['sample_text']}
Feature area: {issue['feature_area']}
Review count: {issue['frequency']}
Error correlation: {issue['error_spike_ratio']}x baseline error rate
Priority score: {issue['priority_score']:.2f}

Sample user quotes:
{chr(10).join('- ' + q[:150] for q in sample_quotes)}

Include: Title, Priority, Description, Likely repro steps (inferred), Evidence, Recommended action."""

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        content = completion.choices[0].message.content
        with open(f"outputs/reports/issue_{int(issue['cluster_id'])}.md", 'w') as f:
            f.write(content)
        print(f"Generated report for cluster {issue['cluster_id']}")
    except Exception as e:
        print(f"Failed on cluster {issue['cluster_id']}: {e}")
    time.sleep(2)

print("Done — reports in outputs/reports/")
