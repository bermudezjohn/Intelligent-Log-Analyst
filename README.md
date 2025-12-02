# 🛡️ Intelligent Log Analyst (AI-Powered SIEM Helper)

## 📌 Project Overview
Security Operations Center (SOC) analysts often face "alert fatigue," dealing with thousands of log lines daily. This project demonstrates how **Machine Learning** can automate the detection of network anomalies and group repetitive logs, allowing analysts to focus on genuine threats.

I built a Python-based tool that:
1.  **Parses** raw Linux system logs (syslog/auth.log).
2.  **Vectorizes** log messages using **TF-IDF** (Term Frequency-Inverse Document Frequency).
3.  **Detects Anomalies** using **Isolation Forest** (Unsupervised Learning) to flag rare, suspicious events.
4.  **Clusters** routine traffic using **K-Means**, helping to categorize "noise."

## 🚀 Features
- **Automated Parsing:** Regex handling for standard syslog formats.
- **Smart Preprocessing:** Masks dynamic data (IPs, PIDs, Timestamps) to generalize log patterns.
- **Unsupervised Anomaly Detection:** No labeled data required; the model learns what "normal" looks like and flags deviations.
- **Cluster Analysis:** Groups similar logs together to help analysts identify routine background noise.

## 🛠️ Technologies Used
- **Language:** Python 3.9+
- **Libraries:** Pandas, Scikit-learn, NumPy, Regex
- **Concepts:** Natural Language Processing (NLP), Anomaly Detection, Clustering

## 💻 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/bermudezjohn/Intelligent-Log-Analyst.git
cd Intelligent-Log-Analyst
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the analyzer
```bash
python log_analyst.py
```
### 📊 Sample Output
When running against the provided ```sample_logs.log```, the tool successfully identifies the hidden buffer overflow attack and categorizes the routine traffic.

**Anomaly Detection:**
```bash
🚨 ANOMALY REPORT: Found 3 suspicious events
==================================================
Timestamp       Process                                                        Message
Dec 10 08:15:22 sshd[9999]: CORE DUMP: Buffer overflow detected at memory address 0x44414141
Dec 10 08:15:23 kernel:     [1234.5678] Segfault in python3 at ip 00007f302222 error 4
Dec 10 08:15:25 sshd[9999]: Possible exploit attempt: shell code detected in input stream
```
**Clustering (Noise Reduction):**
```bash
Cluster 0 Sample Logs (Routine CRON jobs):
(root) CMD (cd / && run-parts --report /etc/cron.hourly)
(root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)

Cluster 1 Sample Logs (SSH Failures):
Failed password for invalid user root from 10.0.0.5 port 44222 ssh2
```
### 🧠 Why This Matters for Cybersecurity
Traditional SIEMs rely on static rules (e.g., ```if "error" in log: alert()```). However, zero-day attacks often generate logs that don't match known signatures but statistically look different from normal traffic. This project proves that AI can catch these "unknown unknowns" without human intervention.
