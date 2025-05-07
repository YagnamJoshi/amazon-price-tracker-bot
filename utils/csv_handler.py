import pandas as pd
import os

# Change the path to store CSV in the 'data' folder
DATA_FOLDER = 'data'
CSV_FILE = os.path.join(DATA_FOLDER, 'product_data.csv')

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        os.makedirs(DATA_FOLDER, exist_ok=True)  # Create the 'data' folder if it doesn't exist
        df = pd.DataFrame(columns=['user_id', 'product_url', 'target_price'])
        df.to_csv(CSV_FILE, index=False)

def add_product(user_id, product_url, target_price):
    initialize_csv()
    df = pd.read_csv(CSV_FILE)
    # Check if the product already exists for the user
    if df[(df['user_id'] == user_id) & (df['product_url'] == product_url)].empty:
        new_entry = {'user_id': user_id, 'product_url': product_url, 'target_price': target_price}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
    else:
        print(f"Product already tracked for user {user_id}: {product_url}")

def get_user_products(user_id):
    initialize_csv()
    df = pd.read_csv(CSV_FILE)
    user_products = df[df['user_id'] == user_id]
    return user_products

def delete_user_product(user_id, product_url):
    initialize_csv()
    df = pd.read_csv(CSV_FILE)
    # Remove the product for the user
    df = df[~((df['user_id'] == user_id) & (df['product_url'] == product_url))]
    if len(df) < len(pd.read_csv(CSV_FILE)):  # If something was deleted
        df.to_csv(CSV_FILE, index=False)
        return True
    return False
