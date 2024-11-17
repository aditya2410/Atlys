import json
from app.storage.storage_strategy import StorageStrategy

class JSONStorage(StorageStrategy):
    def __init__(self, file_path="scraped_data.json"):
        self.file_path = file_path

    def save_product(self, title: str, price: str, image_path: str):
        try:
            data = self.fetch_products()
        except FileNotFoundError:
            data = []

        product = {
            "product_title": title,
            "product_price": price,
            "path_to_image": image_path,
        }

        # Avoid duplicates
        if product not in data:
            data.append(product)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def fetch_products(self):
        with open(self.file_path, "r") as f:
            return json.load(f)
