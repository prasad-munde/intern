from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

# Define URLs by label
urls = {
    "login": [
        "https://github.com/login",
        "https://accounts.google.com/signin",
        "https://www.facebook.com/login"
    ],
    "home": [
        "https://www.google.com",
        "https://www.facebook.com",
        "https://twitter.com"
    ]
}

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")  # newer headless mode (more stable)
options.add_argument("--window-size=1920,1080")  # ensure large enough to see full page
driver = webdriver.Chrome(options=options)

# Base output directory
base_dir = "dataset"

# Create folders
for label in urls.keys():
    folder_path = os.path.join(base_dir, label)
    os.makedirs(folder_path, exist_ok=True)

# Loop through each label and URL
for label, url_list in urls.items():
    for i, url in enumerate(url_list):
        try:
            print(f"Opening: {url}")
            driver.get(url)
            time.sleep(3)  # wait for full load

            file_path = os.path.join(base_dir, label, f"{label}_{i+1}.png")
            driver.save_screenshot(file_path)
            print(f"Saved screenshot → {file_path}")
        except Exception as e:
            print(f"❌ Error loading {url}: {e}")

driver.quit()
print("✅ All screenshots complete.")
