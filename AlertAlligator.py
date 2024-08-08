#!/usr/bin/python3

from datetime import datetime, timezone
import feedparser
from pymsteams import connectorcard

WEBHOOK_URL = 'YOUR_WEBHOOK'

def scraper() -> list:
    news_feed = feedparser.parse("https://www.cert.ssi.gouv.fr/feed/")
    entries_today = []
    today = datetime.now(timezone.utc).date()

    for entry in news_feed.entries:
        entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").date()
        if str(entry_date) == str(today):
            entry_data = {
                "Title": entry.title.rsplit("(", 1)[0],
                "Date": entry.title.rsplit("(", 1)[1].rsplit(")", 1)[0],
                "Link": entry.link
            }
            entries_today.append(entry_data)
    return entries_today

def send_teams_message(results):
    for result in results:
        card = connectorcard(WEBHOOK_URL)
        card.title(result["Title"])
        card.text(f"Date: {result['Date']}")
        card.addLinkButton("Link", result["Link"])
        card.send()

def main():
    results = scraper()
    send_teams_message(results)

if __name__ == "__main__":
    main()
