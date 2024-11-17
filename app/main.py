from fastapi import FastAPI, HTTPException, Header
from app.notifications.console_notifier import ConsoleNotifier
from app.scraper import Scraper
from app.cache import Cache
from app.settings import Settings
from app.models import ScrapeSettings
from app.notifications.composite_notifier import CompositeNotifier
from app.storage.json_storage import JSONStorage


app = FastAPI()

settings = Settings()
# Configure cache and storage
cache = Cache(redis_url="redis://localhost")
storage = JSONStorage(file_path="scraped_data.json")

notifiers = [
    ConsoleNotifier(),
]
composite_notifier = CompositeNotifier(notifiers)
scraper = Scraper(storage=storage, cache=cache, notifier=composite_notifier)


@app.post("/scrape/")
async def scrape(
    scrape_settings: ScrapeSettings,
    authorization: str = Header(...),
):
    if authorization != f"Bearer {settings.auth_token}":
        raise HTTPException(status_code=401, detail="Invalid token")
    
    result = await scraper.scrape_catalogue(scrape_settings, max_retries=3)
    return {"status": "success", "products_scraped": result}


