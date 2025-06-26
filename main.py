# Import necessary libraries
from flask import Flask, render_template
import requests
from datetime import datetime
import pytz  # For Pakistan timezone
import time  # For delay
import os  # To check/create log file
import threading  # For background scheduler

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Initialize Flask application
app = Flask(__name__)

# Websites to archive
websites_to_archive = [
    "https://akhuwat.org.pk", 
    "https://akhuwat.edu.pk",
    "https://donate.akhuwat.org.pk", 
    "https://ahfcl.org.pk",
    "https://amjadsaqib.com", 
    "https://akhuwatislamicmicrofinance.org.pk",
    "https://freelancers.akhuwat.edu.pk"
]

# Log file path
log_file = "archive_log.txt"

def archive_url(url):
    save_url = f"https://web.archive.org/save/{url}"
    headers = {"User-Agent": "Mozilla/5.0 (WaybackArchiverBot)"}
    now = datetime.now(pytz.timezone('Asia/Karachi')).strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.get(save_url, headers=headers)

        if response.status_code == 200:
            msg = f"[{now}] ✅ Archived: {url}"
            print(f"{GREEN}{msg}{RESET}")
        else:
            msg = f"[{now}] ❌ Failed: {url} (Status: {response.status_code})"
            print(f"{RED}{msg}{RESET}")

    except Exception as e:
        msg = f"[{now}] ❌ Error: {url} ({str(e)})"
        print(f"{RED}{msg}{RESET}")

    # Save to log
    with open(log_file, "a") as f:
        f.write(msg + "\n")

    return msg

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/archive')
def archive():
    results = []
    for url in websites_to_archive:
        result = archive_url(url)
        results.append(result)
        time.sleep(2)
    return "\n".join(results)

# 🔁 Auto-archiving loop (every X minutes)
def auto_archive_loop(interval_minutes=60):
    def run_archiver():
        print("🔁 Auto archive running in background...")
        for url in websites_to_archive:
            archive_url(url)
        threading.Timer(interval_minutes * 60, run_archiver).start()
    run_archiver()

if __name__ == '__main__':
    auto_archive_loop(60)  # Runs every 60 minutes
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
