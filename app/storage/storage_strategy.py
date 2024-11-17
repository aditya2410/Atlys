from abc import ABC, abstractmethod


class StorageStrategy(ABC):
    @abstractmethod
    def save_product(self, title: str, price: str, image_path: str):
        pass

    @abstractmethod
    def fetch_products(self):
        pass
