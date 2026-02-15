# ultra_simple_scraper.py
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from datetime import datetime


def setup_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            url TEXT,
            features TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database ready")


def scrape_product(url):
    print(f"\n Scraping {url}")
    

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    name = soup.find('h3')
    name = name.text.strip() if name else "Unknown"
    
    
    price = soup.find('span', class_='product-price')
    price = price.text.strip() if price else "N/A"
    
    
    features = {}
    table = soup.find('div', class_='vertical-table')
    if table:
        rows = table.find_all('div', class_='vertical-table-row')
        for row in rows:
            key = row.find('div', class_='vertical-table-header')
            val = row.find('div', class_='vertical-table-cell')
            if key and val:
                features[key.text.strip()] = val.text.strip()
    
    
    features_json = json.dumps(features)
    
    print(f"Found: {name} - {price}")
    return (name, price, url, features_json, datetime.now().strftime('%Y-%m-%d %H:%M'))

def save_product(product_data):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO products (name, price, url, features, date)
        VALUES (?, ?, ?, ?, ?)
    ''', product_data)
    conn.commit()
    conn.close()
    print(f"Saved to database")

def show_all_products():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price, date FROM products')
    products = cursor.fetchall()
    conn.close()
    
    print("\n" + "="*60)
    print("PRODUCTS IN DATABASE")
    print("="*60)
    for p in products:
        print(f"ID: {p[0]} | {p[1][:20]:<20} | {p[2]:<15} | {p[3]}")
    print("="*60)


def show_product_details(product_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    p = cursor.fetchone()
    conn.close()
    
    if p:
        print("\n" + "="*50)
        print(f"PRODUCT #{p[0]}")
        print("="*50)
        print(f"Name: {p[1]}")
        print(f"Price: {p[2]}")
        print(f"URL: {p[3]}")
        print(f"Features: {json.loads(p[4])}")
        print(f"Scraped: {p[5]}")
        print("="*50)
    else:
        print(f"No product with ID {product_id}")


def export_csv():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    
    with open('products.csv', 'w') as f:
        f.write('ID,Name,Price,URL,Features,Date\n')
        for p in products:
            f.write(f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]},{p[5]}\n")
    print("Exported to products.csv")

def export_json():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    
    data = []
    for p in products:
        data.append({
            'id': p[0],
            'name': p[1],
            'price': p[2],
            'url': p[3],
            'features': json.loads(p[4]),
            'date': p[5]
        })
    
    with open('products.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Exported to products.json")


def main():
    setup_db()
    
    while True:
        print("\n" + "="*40)
        print("PRODUCT SCRAPER MENU")
        print("="*40)
        print("1. Scrape new product")
        print("2. Show all products")
        print("3. View product details")
        print("4. Export to CSV")
        print("5. Export to JSON")
        print("6. Exit")
        print("-"*40)
        
        choice = input("Choose (1-6): ").strip()
        
        if choice == '1':
            url = input("Enter product URL (or press Enter for default): ").strip()
            if not url:
                url = "https://web-scraping.dev/product/1"
            try:
                product = scrape_product(url)
                save_product(product)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            show_all_products()
        
        elif choice == '3':
            try:
                pid = int(input("Enter product ID: "))
                show_product_details(pid)
            except:
                print("Invalid ID")
        
        elif choice == '4':
            export_csv()
        
        elif choice == '5':
            export_json()
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice")



main()