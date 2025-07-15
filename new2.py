import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# ---------- CONFIG ----------
START_INDEX = 941  # Resume from 941st row (0-based index)
BROWSER_RESET_INTERVAL = 100  # restart browser every N rows
PAGE_TIMEOUT = 15  # seconds
SCREENSHOT_DIR = "dataset"
CSV_FILE = "urls.csv"
# ---------------------------

# Load the CSV, skipping first 940 URLs
df = pd.read_csv(CSV_FILE, skiprows=range(1, START_INDEX))  # skip header + 940 rows

# Browser options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")

# Initialize browser
driver = webdriver.Chrome(options=options)

def reset_browser():
    global driver
    try:
        driver.quit()
    except:
        pass
    driver = webdriver.Chrome(options=options)

# Loop over remaining rows
for i, row in enumerate(df.itertuples(), start=START_INDEX):
    label = row.label
    url = row.url

    # Restart browser every N rows
    if (i - START_INDEX) % BROWSER_RESET_INTERVAL == 0 and i > START_INDEX:
        print("🔁 Restarting browser to avoid memory leaks...")
        reset_browser()

    try:
        driver.set_page_load_timeout(PAGE_TIMEOUT)

        # Create subfolder (login/home/...)
        label_folder = os.path.join(SCREENSHOT_DIR, label)
        os.makedirs(label_folder, exist_ok=True)

        print(f"[{i}] Visiting: {url}")
        driver.get(url)
        time.sleep(3)

        # Save screenshot
        file_path = os.path.join(label_folder, f"{label}_{i}.png")
        driver.save_screenshot(file_path)
        print(f"✓ Saved: {file_path}")

    except TimeoutException:
        print(f"⏱️ Timeout: {url}")
        continue
    except Exception as e:
        print(f"× Failed: {url} — {e}")
        continue

# Clean up
driver.quit()
print("✅ Finished remaining screenshots.")
