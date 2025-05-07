import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = 'product_data.csv'
SCRAPPER_API = os.getenv("SCRAPPER_API")
SCRAPPER_URL = os.getenv("SCRAPPER_URL")

def check_prices():
    """Check prices of all tracked products and notify users."""
    if not os.path.exists(CSV_FILE):
        print("⚠️ No products to track yet.")
        return

    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("⚠️ No products to track yet.")
        return

    for index, row in df.iterrows():
        user_id = row['user_id']
        product_url = row['product_url']
        target_price = float(row['target_price'])

        params = {
            'api_key': SCRAPPER_API,
            'url': product_url
        }
        response = requests.get(SCRAPPER_URL, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                product_name = soup.find('span', class_='a-size-large product-title-word-break').text.strip()
                price_text = soup.find('span', class_='a-price-whole').text
                price = float(price_text.replace(',', '').strip())

                if price <= target_price:
                    print(f"✅ User {user_id}: '{product_name}' dropped to ₹{price} (Target was ₹{target_price})")
                else:
                    print(f"🔔 User {user_id}: '{product_name}' is still ₹{price} (Target was ₹{target_price})")

            except Exception as e:
                print(f"❌ Failed to scrape {product_url}: {e}")
        else:
            print(f"❌ Failed to fetch data for {product_url} (Status Code: {response.status_code})")

if __name__ == "__main__":
    check_prices()
