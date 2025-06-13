import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/bio-wellness-444-llc-709333-05302025"
SAVE_DIR = "data/fda_letters"
FILENAME = "bio_wellness_444_llc_709333_05302025.txt"

os.makedirs(SAVE_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

resp = requests.get(URL, headers=headers)
if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    path = os.path.join(SAVE_DIR, FILENAME)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Saved letter to {path}")
else:
    print(f"❌ Failed to fetch letter. HTTP Status: {resp.status_code}")
