import requests
import time

TELEGRAM_TOKEN = "7759695922:AAGlvkW9TAYC1kjtp4CDU3BkVe0X5fIgN1M"
CHAT_ID = "1390912843"

sent_jobs = set()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending Telegram message:", e)

# Example companies (Greenhouse + Lever endpoints)
companies = {
    "google": "https://boards.greenhouse.io/api/v1/boards/google/jobs",   # Greenhouse
    "lever": "https://api.lever.co/v0/postings/leverdemo?mode=json"       # Lever (demo)
}

def fetch_greenhouse_jobs(url):
    try:
        resp = requests.get(url)
        data = resp.json()
        jobs = data.get("jobs", [])
        return [(job["id"], job["title"], job["absolute_url"]) for job in jobs]
    except Exception as e:
        print("Error fetching Greenhouse jobs:", e)
        return []

def fetch_lever_jobs(url):
    try:
        resp = requests.get(url)
        data = resp.json()
        return [(job["id"], job["text"], job["hostedUrl"]) for job in data]
    except Exception as e:
        print("Error fetching Lever jobs:", e)
        return []

def check_jobs():
    # Google Jobs (Greenhouse)
    google_jobs = fetch_greenhouse_jobs(companies["google"])
    new_google = []
    for jid, title, link in google_jobs[:5]:
        if jid not in sent_jobs:
            sent_jobs.add(jid)
            new_google.append((title, link))
    if new_google:
        msg = "📢 <b>New Google Job Openings</b>\n\n"
        for title, link in new_google:
            msg += f"• <a href='{link}'>{title}</a>\n"
        send_to_telegram(msg)

    # Lever Jobs
    lever_jobs = fetch_lever_jobs(companies["lever"])
    new_lever = []
    for jid, title, link in lever_jobs[:5]:
        if jid not in sent_jobs:
            sent_jobs.add(jid)
            new_lever.append((title, link))
    if new_lever:
        msg = "📢 <b>New Lever Job Openings (Demo)</b>\n\n"
        for title, link in new_lever:
            msg += f"• <a href='{link}'>{title}</a>\n"
        send_to_telegram(msg)


print("🚀 Auto Job Tracker Started...\n")
while True:
    check_jobs()
    print("✅ Checked for new jobs. Waiting 30 mins...")
    time.sleep(1800)  # 30 minutes (1800 sec)