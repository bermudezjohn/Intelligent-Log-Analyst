import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
LOG_FILE = 'sample_logs.log'
ANOMALY_THRESHOLD = 0.05 # Top 5% are considered anomalies

def parse_logs(filepath):
    r"""
    Parses a standard Linux syslog file into a Pandas DataFrame.
    Regex explained:
    ^(\w{3}\s+\d+\s\d+:\d+:\d+) -> Date/Time (e.g., Dec 10 06:55:01)
    \s
    (\w+) -> Hostname (e.g., server1)
    \s
    (.*?): -> Process Name (e.g., sshd[1234]:)
    \s
    (.*)$ -> The Log Message
    """
    log_pattern = re.compile(r'^(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\s(.*?):\s(.*)$')

    data = []
    with open(filepath, 'r') as f:
        for line in f:
            match = log_pattern.match(line.strip())
            if match:
                data.append(match.groups())

    return pd.DataFrame(data, columns=['Timestamp', 'Host', 'Process', 'Message'])

def preprocess_text(text):
    """
    Cleans log messages to make them better for clustering.
    Replaces specific numbers/IPs with placeholders so 'User 1' and 'User 2'
    look the same to the AI.
    """
    # Replace IP addresses with <IP>
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', text)
    # Replace Hex memory addresses (common in errors) with <MEM>
    text = re.sub(r'0x[0-9a-fA-F]+', '<MEM>', text)
    # Replace generic numbers with <NUM>
    text = re.sub(r'\d+', '<NUM>', text)
    return text

def analyze_logs():
    print("Step 1: Parsing logs...")
    df = parse_logs(LOG_FILE)
    print(f"Parsed {len(df)} log lines.")

    print("Step 2: Preprocessing text...")
    df['Clean_Message'] = df['Message'].apply(preprocess_text)

    # Convert text to numbers using TF-IDF (Term Frequency-Inverse Document Frequency)
    # This highlights unique words while ignoring common ones like "the" or "for"
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Clean_Message'])

    print("Step 3: Detecting Anomalies using Isolation Forest...")
    # Isolation Forest is great for detecting "outliers" (rare events)
    iso_forest = IsolationForest(contamination=ANOMALY_THRESHOLD, random_state=42)
    df['Anomaly'] = iso_forest.fit_predict(X.toarray())

    # IsolationForest returns -1 for anomalies, 1 for normal
    anomalies = df[df['Anomaly'] == -1]

    print("\n" + "="*50)
    print(f"🚨 ANOMALY REPORT: Found {len(anomalies)} suspicious events")
    print("="*50)

    if not anomalies.empty:
        print(anomalies[['Timestamp', 'Process', 'Message']].to_string(index=False))
    else:
        print("No anomalies detected. System looks clean!")

    print("\n" + "="*50)
    print("📊 CLUSTERING REPORT (Grouping similar logs)")
    print("="*50)

    # Use K-Means to group normal traffic for easy review
    # We guess 3 clusters for this small sample (Cron, SSH Login, SSH Fail)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    # Print a few examples from each cluster
    for i in range(3):
        print(f"\nCluster {i} Sample Logs:")
        cluster_samples = df[df['Cluster'] == i].head(3)
        print(cluster_samples['Message'].to_string(index=False))

if __name__ == "__main__":
    analyze_logs()