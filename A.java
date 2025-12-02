🛡️ Intelligent Log Analyst (AI-Powered SIEM Helper)

📌 Project Overview

Security Operations Center (SOC) analysts often face "alert fatigue," dealing with thousands of log lines daily. This project demonstrates how Machine Learning can automate the detection of network anomalies and group repetitive logs, allowing analysts to focus on genuine threats.

I built a Python-based tool that:

Parses raw Linux system logs (syslog/auth.log).

Vectorizes log messages using TF-IDF (Term Frequency-Inverse Document Frequency).

Detects Anomalies using Isolation Forest (Unsupervised Learning) to flag rare, suspicious events.

Clusters routine traffic using K-Means, helping to categorize "noise."

🚀 Features

Automated Parsing: Regex handling for standard syslog formats.

Smart Preprocessing: Masks dynamic data (IPs, PIDs, Timestamps) to generalize log patterns.

Unsupervised Anomaly Detection: No labeled data required; the model learns what "normal" looks like and flags deviations.

🛠️ Technologies Used

Language: Python 3.9+

Libraries: Pandas, Scikit-learn, NumPy, Regex

Concepts: Natural Language Processing (NLP), Anomaly Detection, Clustering

💻 How to Run

Clone the repository:

git clone [https://github.com/yourusername/intelligent-log-analyst.git](https://github.com/yourusername/intelligent-log-analyst.git)
cd intelligent-log-analyst


Install dependencies:

pip install -r requirements.txt


Run the analyzer:

python log_analyst.py


📊 Sample Output

When running against the sample_logs.log, the tool successfully identifies the hidden buffer overflow attack:

🚨 ANOMALY REPORT: Found 3 suspicious events
==================================================
Timestamp       Process                                                        Message
Dec 10 08:15:22 sshd[9999]: CORE DUMP: Buffer overflow detected at memory address 0x44414141
Dec 10 08:15:23 kernel:     [1234.5678] Segfault in python3 at ip 00007f302222 error 4
Dec 10 08:15:25 sshd[9999]: Possible exploit attempt: shell code detected in input stream


🧠 Why This Matters for Cybersecurity

Traditional SIEMs rely on static rules (e.g., if "error" in log: alert()). However, zero-day attacks often generate logs that don't match known signatures but statistically look different from normal traffic. This project proves that AI can catch these "unknown unknowns."