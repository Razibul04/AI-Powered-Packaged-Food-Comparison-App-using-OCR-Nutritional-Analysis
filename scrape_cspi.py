import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Health score mapping
rating_to_score = {
    'Safe': 90,
    'Cut Back': 70,
    'Caution': 50,
    'Avoid': 20,
    'Certain People Should Avoid': 40
}

# Base URL
base_url = 'https://www.cspinet.org/page/additives-contaminants'

# Fetch main list page
print("🔍 Fetching additive list...")
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Try multiple selector paths if needed
entries = soup.select('.views-row a[href]')

if not entries:
    print("❌ No entries found on the CSPI page. The structure might have changed.")
    exit()

additives = []

for idx, link in enumerate(entries):
    name = link.text.strip()
    href = link.get("href")
    if not href:
        continue

    detail_url = "https://www.cspinet.org" + href
    print(f"➡️  [{idx+1}] Processing: {name}")

    detail_response = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

    # Try to extract rating
    rating_tag = detail_soup.select_one('.field-name-field-additive-rating .field-item')
    rating = rating_tag.get_text(strip=True) if rating_tag else "Unknown"
    health_score = rating_to_score.get(rating, 50)

    # Try to extract category
    category_tag = detail_soup.select_one('.field-name-field-additive-category .field-item')
    category = category_tag.get_text(strip=True) if category_tag else "Unknown"

    # Try to extract aliases
    aliases_tag = detail_soup.select_one('.field-name-field-additive-aliases .field-item')
    aliases = aliases_tag.get_text(strip=True) if aliases_tag else "Unknown"

    # Try to extract health concerns
    concern_tag = detail_soup.select_one('.field-name-field-additive-concerns .field-item')
    concern = concern_tag.get_text(strip=True) if concern_tag else "Not specified"

    additives.append({
        'ingredient': name,
        'category': category,
        'aliases': aliases,
        'health concern': concern,
        'health score': health_score
    })

    time.sleep(1)  # Be nice to the server

# Save to CSV
if additives:
    df = pd.DataFrame(additives)
    df.to_csv("cspi_food_additives.csv", index=False)
    print("✅ Saved to 'cspi_food_additives.csv'")
else:
    print("⚠️ No data extracted — check page structure or scraping logic.")
