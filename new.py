import csv
import re

input_file = "start.txt"
output_file = "urls.csv"
login_paths = ["/login", "/signin", "/account/login"]

domains = []

# Step 1: Extract domains from start.txt
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            domain = parts[1]
            # Basic domain format validation
            if re.match(r"^[\w.-]+\.[a-z]{2,}$", domain.lower()):
                domains.append(domain.lower())

# Remove duplicates
unique_domains = sorted(set(domains))

# Step 2: Write to urls.csv with labels
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["label", "url"])
    for domain in unique_domains:
        writer.writerow(["home", f"https://{domain}"])
        for path in login_paths:
            writer.writerow(["login", f"https://{domain}{path}"])

print(f"✅ Extracted {len(unique_domains)} domains")
print(f"📁 Generated {output_file} with ~{len(unique_domains) * 4} URLs")
