# AI Product Reliability & Feedback Intelligence

Turns messy, unstructured user feedback into a prioritized, developer-ready backlog by classifying, clustering, and correlating reviews with product error signals.

## Problem
Product teams drown in scattered feedback (app reviews, tickets, forums) with no systematic way to separate signal from noise or connect it to what's actually breaking in production.

## Approach
1. Scraped 1,600 real Play Store reviews across 2 apps (Swiggy, PhonePe)
2. Classified reviews into bug / feature request / UX issue / noise using an LLM pipeline (Groq, Llama-based model)
3. Clustered duplicates using TF-IDF + K-Means, collapsing ~300 actionable reviews into 25 distinct issue clusters
4. Correlated clusters against synthetic backend error-event data to validate real-world impact
5. Scored and ranked issues using a transparent weighted formula (frequency, error correlation, severity, confidence)
6. Auto-generated developer-ready issue reports for the top 5 priority clusters

## Key findings
- Payment gateway fraud/duplicate-charge complaints (18 reviews) correlated with a 122.5x spike in backend payment errors, the single highest-priority issue, previously buried in aggregate app ratings
- Checkout refund issues (16 reviews) showed a 93x error spike, the second most urgent cluster
- Most other complaint categories (order tracking, login) showed no meaningful error correlation (1.5x or less), useful signal that these are perception/experience issues rather than backend failures

## Architecture
Scrape (Play Store) -> Classify (LLM) -> Cluster (TF-IDF + KMeans) -> Correlate (error events) -> Score -> Generate Reports

## Tech stack
Python, Groq API (Llama/GPT-OSS models), scikit-learn, pandas

## Run it yourself
pip install -r requirements.txt
python scripts/01_scrape_reviews.py
python scripts/02_generate_errors.py
python scripts/03_classify.py
python scripts/04_cluster.py
python scripts/05_correlate.py
python scripts/06_score.py
python scripts/07_generate_reports.py

## Sample output
See outputs/ranked_issues.csv for the full prioritized backlog, and outputs/reports/ for auto-generated developer-ready issue reports.
