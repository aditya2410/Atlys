import sqlite3
from app.storage.storage_strategy import StorageStrategy

class SQLiteStorage(StorageStrategy):
    def __init__(self, db_path="scraped_data.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_title TEXT UNIQUE,
                product_price TEXT,
                path_to_image TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_product(self, title: str, price: str, image_path: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO products (product_title, product_price, path_to_image)
            VALUES (?, ?, ?)
        """, (title, price, image_path))
        conn.commit()
        conn.close()

    def fetch_products(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT product_title, product_price, path_to_image FROM products")
        products = cursor.fetchall()
        conn.close()
        return [
            {"product_title": title, "product_price": price, "path_to_image": path}
            for title, price, path in products
        ]