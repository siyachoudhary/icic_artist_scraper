from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Setup
# use this if you have mac intel chip
service = Service(executable_path='./chromedriver-mac-x64/chromedriver')
# use this if you have mac M1,M2... chip
# service = Service(executable_path='./chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

base_url = "https://pakmag.net/film/artist.php?pid="
all_people = []

max_pid = 4700  # adjust as needed
fail_streak = 0
max_fail_streak = 5  # stop if we hit 50 bad pages in a row

for pid in range(1, max_pid + 1):
    url = base_url + str(pid)
    driver.get(url)
    time.sleep(1)

    try:
        # grab artist name from the main heading (usually inside h1)
        heading = driver.find_element(By.TAG_NAME, 'h1').text.strip()

        if heading == "":  # page exists but no name
            raise Exception("Empty page")

        all_people.append((heading, url))
        print(f"Found: {heading} — {url}")
        fail_streak = 0  # reset streak on success
    except:
        print(f"Not found: pid={pid}")
        fail_streak += 1
        if fail_streak >= max_fail_streak:
            print("Too many consecutive failures — stopping.")
            break

# Save
with open('pakmag_all_people_by_pid.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Profile URL'])
    writer.writerows(all_people)

driver.quit()
print(f"Finished scraping {len(all_people)} people.")
