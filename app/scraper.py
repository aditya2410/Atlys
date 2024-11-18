import httpx
from bs4 import BeautifulSoup
import aiofiles
from app.storage.storage_strategy import StorageStrategy
from app.cache import Cache
from app.notifications.notifier import Notifier
import time
import os


class Scraper:
    def __init__(self, storage: StorageStrategy, cache: Cache, notifier: Notifier):
        self.storage = storage
        self.cache = cache
        self.notifier = notifier

    async def scrape_catalogue(self, settings, max_retries):
        headers = {"User-Agent": "Mozilla/5.0"}
        products= []

        attempt = 0
        for page in range(1, settings.max_pages + 1):
            url = f"https://dentalstall.com/shop/page/{page}/"
            while attempt < max_retries:
                try:
                    async with httpx.AsyncClient(follow_redirects=True, proxies=settings.proxy) as client:
                        response = await client.get(url, headers=headers)
                        response.raise_for_status()

                    soup = BeautifulSoup(response.text, "html.parser")

                    productSoup = soup.find('ul', class_ = "products columns-4").find_all('li')

                    # Iterate through each product
                    for product in productSoup:
                        # Extract product name
                        try:
                            product_name_element = product.find('div', class_="addtocart-buynow-btn")
                            product_name = product_name_element.find('a').get('data-title')
                            # Extract product price
                            product_price = product.find('div', class_="mf-product-price-box").find('bdi').text.strip()
                            price_float = float(product_price.replace('\u20b9', ''))
                            # Extract product image URL
                            image_element = product.find('div', class_="mf-product-thumbnail").find('a').find('img')
                            product_image_url = image_element.get('data-lazy-src')
                        except AttributeError:
                            continue

                        if self.cache.is_cached(product_name, product_price):
                            continue

                        # Download image
                        image_path = await self._download_image(product_image_url, product_name)
                        products.append({
                            "name": product_name,
                            "price": price_float,
                            "img": image_path
                        })
                        
                        self.storage.save_product(price=price_float, image_path=image_path, title=product_name)
                        self.cache.update_cache(product_name, product_price)
                    
                    break
                except httpx.RequestError:
                    time.sleep(5)  # Retry delay
                    attempt+=1
                    continue

        message = f"Scraping completed. {len(products)} products updated."
        self.notifier.notify(message)
        return len(products)

    async def _download_image(self, img_url, title):
        async with httpx.AsyncClient() as client:
            response = await client.get(img_url)
            path = f"images/{title.replace(' ', '_')}.jpg"

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)  # exist_ok prevents errors if directory exists

            async with aiofiles.open(path, "wb") as f:
                await f.write(response.content)
        return path