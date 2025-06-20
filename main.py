# Import necessary libraries
from flask import Flask, render_template
import requests
from datetime import datetime
import pytz  # For Pakistan timezone
import time  # For delay
import os  # To check/create log file

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Initialize Flask application
app = Flask(__name__)

# Websites to archive
websites_to_archive = [
    "https://akhuwat.org.pk", "https://akhuwat.edu.pk",
    "https://donate.akhuwat.org.pk", "https://ahfcl.org.pk",
    "https://amjadsaqib.com", "https://akhuwatislamicmicrofinance.org.pk"
]

# Log file path
log_file = "archive_log.txt"

def archive_url(url):
    """
    Archive a single URL using the Wayback Machine Save API
    and log result to console and file
    """
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

    # Save message to log file
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
        time.sleep(2)  # Delay between requests
    return "\n".join(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
