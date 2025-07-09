# Import necessary libraries
from flask import Flask, render_template  # Flask web framework and HTML rendering
import requests  # To make HTTP requests to Wayback Machine
from datetime import datetime  # To get current time
import pytz  # For timezone handling (Asia/Karachi)
import time  # For delays and sleep
import os  # To access environment variables and file operations
import threading  # To run background tasks (scheduler)
import schedule  # To run jobs at specific times

# Terminal colors for output (green for success, red for error, reset for normal text)
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Initialize Flask web application
app = Flask(__name__)

# List of websites to archive
websites_to_archive = [
    "https://akhuwat.org.pk", "https://akhuwat.edu.pk",
    "https://donate.akhuwat.org.pk", "https://ahfcl.org.pk",
    "https://amjadsaqib.com", "https://akhuwatislamicmicrofinance.org.pk",
    "https://freelancers.akhuwat.edu.pk"
]

# File path to save archive logs
log_file = "archive_log.txt"


# Function to archive a given URL using the Wayback Machine
def archive_url(url):
    save_url = f"https://web.archive.org/save/{url}"  # Wayback Machine save endpoint
    headers = {
        "User-Agent": "Mozilla/5.0 (WaybackArchiverBot)"
    }  # Set a bot-like User-Agent
    now = datetime.now(pytz.timezone('Asia/Karachi')).strftime(
        "%Y-%m-%d %H:%M:%S")  # Current time in PK format

    try:
        response = requests.get(save_url,
                                headers=headers)  # Send request to archive URL

        # If request was successful
        if response.status_code == 200:
            msg = f"[{now}] ✅ Archived: {url}"  # Log success message
            print(f"{GREEN}{msg}{RESET}")  # Print success in green
        else:
            msg = f"[{now}] ❌ Failed: {url} (Status: {response.status_code})"  # Log failure
            print(f"{RED}{msg}{RESET}")  # Print failure in red

    # If an error occurred during request
    except Exception as e:
        msg = f"[{now}] ❌ Error: {url} ({str(e)})"  # Log error message
        print(f"{RED}{msg}{RESET}")  # Print error in red

    # Append the message to log file
    with open(log_file, "a") as f:
        f.write(msg + "\n")

    return msg  # Return message (can be shown in web UI)


# Flask route for homepage
@app.route('/')
def home():
    return render_template(
        'index.html')  # Render an HTML homepage (template required)


# Flask route to manually trigger archiving of all websites
@app.route('/archive')
def archive():
    results = []  # To store result messages for each site
    for url in websites_to_archive:
        result = archive_url(url)  # Call archiving function
        results.append(result)  # Add result to list
        time.sleep(2)  # Wait 2 seconds to avoid hitting rate limits
    return "\n".join(results)  # Return results as plain text


# Function to run scheduled archiving at specific times
def schedule_archive_jobs():
    # Define exact daily times for auto-archiving (every 4 hours)
    times = ["02:00", "06:00", "10:00", "14:00", "18:00", "22:00"]

    # Schedule archive task at each time
    for t in times:
        schedule.every().day.at(t).do(run_all_archives)  # Schedule job

    # Function to constantly check if it's time to run a job
    def run_scheduler():
        while True:
            schedule.run_pending()  # Run any due jobs
            time.sleep(60)  # Check once per minute

    # Start the scheduler thread in background
    threading.Thread(target=run_scheduler, daemon=True).start()


# Function to run archive for all URLs (used by scheduler)
def run_all_archives():
    print("🕒 Running scheduled archive jobs...")  # Info log
    for url in websites_to_archive:
        archive_url(url)  # Archive each site


# Flask app entry point
if __name__ == '__main__':
    schedule_archive_jobs()  # Start scheduled background tasks
    app.run(host='0.0.0.0', port=int(os.environ.get(
        "PORT",
        8080)))  # Start Flask app on all IPs, port 8080 (or custom from ENV)
