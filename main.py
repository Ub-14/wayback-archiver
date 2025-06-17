
# Import necessary libraries
from flask import Flask, render_template  # Flask for web framework, render_template for HTML rendering
import requests  # For making HTTP requests to the Web Archive API
from datetime import datetime  # For timestamp formatting

# Initialize Flask application
app = Flask(__name__)

# List of websites to archive automatically
# These URLs will be sent to the Wayback Machine for archiving
websites_to_archive = [
    "https://www.akhuwat.org.pk",
    "https://akhuwat.edu.pk",
    "https://donate.akhuwat.org.pk",
    "https://ahfcl.org.pk",
    "https://amjadsaqib.com",
    "https://akhuwatislamicmicrofinance.org.pk"
]

def archive_url(url):
    """
    Archive a single URL using the Wayback Machine Save API
    
    Args:
        url (str): The URL to archive
        
    Returns:
        str: A formatted message indicating success or failure with timestamp
    """
    # Construct the Wayback Machine save URL
    save_url = f"https://web.archive.org/save/{url}"
    
    # Make HTTP GET request to archive the URL
    response = requests.get(save_url)
    
    # Get current timestamp for logging
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if the archiving was successful (HTTP 200 status)
    if response.status_code == 200:
        return f"[{now}] ✅ Archived: {url}"
    else:
        return f"[{now}] ❌ Failed: {url} (Status: {response.status_code})"

@app.route('/')
def home():
    """
    Route handler for the home page
    Renders the main HTML template with the user interface
    """
    return render_template('index.html')  # Load the frontend HTML file

@app.route('/archive')
def archive():
    """
    Route handler for the archiving endpoint
    Processes all websites in the list and returns results
    
    Returns:
        str: Newline-separated results of archiving attempts
    """
    # Archive each URL in the list and collect results
    results = [archive_url(url) for url in websites_to_archive]
    
    # Return results separated by newlines (not HTML breaks)
    # This allows proper parsing by the frontend JavaScript
    return "\n".join(results)

# Start the Flask application
# host='0.0.0.0' makes it accessible from outside the container
# port=8080 is the designated port for this Replit application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
