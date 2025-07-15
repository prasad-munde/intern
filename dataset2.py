import csv
import requests
from bs4 import BeautifulSoup

# Fetch list of top domains from Wikipedia
response = requests.get("https://en.wikipedia.org/wiki/List_of_most-visited_websites")
soup = BeautifulSoup(response.text, "html.parser")

# Parse table rows to extract domain column
domains = []
table = soup.find("table", {"class": "wikitable"})
for row in table.find_all("tr")[1:501]:  # top 500
    cols = row.find_all("td")
    if cols:
        domains.append(cols[1].get_text(strip=True))

print(f"Collected {len(domains)} domains")

# Build CSV of URLs and labels
login_endpoints = ["/login", "/signin", "/account/login"]
with open("urls.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["label", "url"])
    for d in domains:
        home = f"https://{d}"
        writer.writerow(["home", home])
        for path in login_endpoints:
            login_url = f"https://{d}{path}"
            writer.writerow(["login", login_url])
