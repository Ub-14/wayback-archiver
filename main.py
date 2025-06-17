from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

websites_to_archive = [
    "https://www.akhuwat.org.pk",
    "https://akhuwat.edu.pk",
    "https://donate.akhuwat.org.pk",
    "https://ahfcl.org.pk",
    "https://amjadsaqib.com",
    "https://akhuwatislamicmicrofinance.org.pk"
]

def archive_url(url):
    save_url = f"https://web.archive.org/save/{url}"
    response = requests.get(save_url)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response.status_code == 200:
        return f"[{now}] ✅ Archived: {url}"
    else:
        return f"[{now}] ❌ Failed: {url} (Status: {response.status_code})"

@app.route('/')
def home():
    return render_template('index.html')  # frontend load hoga

@app.route('/archive')
def archive():
    results = [archive_url(url) for url in websites_to_archive]
    return "\n".join(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
