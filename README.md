# **Web Scraper with FastAPI**

This project is a web scraping tool built using the **FastAPI** framework. It automates the process of extracting product details (name, price, and image) from [DentalHall](https://dentalstall.com/shop/) and supports flexible configurations such as page limits and proxy usage.

---

## **Features**

1. **Web Scraping:**
   - Scrapes product information including title, price, image URL, and discount percentage.
   - Handles pagination to extract data from multiple pages.

2. **Retry Mechanism:**
   - Retries failed HTTP requests with a configurable retry count and delay for resilience.

3. **Proxy Support:**
   - Supports using a proxy server for scraping.

4. **Authentication:**
   - Ensures secure access using a static token for API endpoints.

5. **Data Storage:**
   - Stores scraped data in a JSON file on the local system.
   - Easily extendable to other storage solutions.

6. **Caching:**
   - Uses an in-memory cache to avoid redundant updates if product data remains unchanged.

7. **Notifications:**
   - Outputs the scraping status (e.g., number of products scraped) via a console notifier.
   - Designed to support other notification systems (e.g., email, Slack) with minimal code changes.

---

## **Technologies Used**

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **HTTP Client:** [httpx](https://www.python-httpx.org/)
- **HTML Parsing:** [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- **Caching:** redis
- **Storage:** JSON file (extensible for other formats like databases)

---

## **Setup and Installation**
for Mac OS or linux
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>

2. **Activate Environment:**
   ```bash
   python -m venv env
   source env/bin/activate 

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt

4. **Run Redis Server:**
   Make sure you have Redis installed and running on your system. To start the Redis server:
    ```bash
    redis-server

4. **Run Fast API application:**
   ```bash
   uvicorn app.main:app --reload

---

## **Usage**
### **API Endpoints**
#### **Scrape Products**
#### **URL**:
       /scrape/
#### **Method**: 
        POST
#### **Authentication**: 
        Requires a static token (configured in the settings.py file).
#### **Payload**: 
      {
        "page_limit": 5,
        "proxy": "http://<proxy_url>"
      }
#### **Response**:
      {
        "status": "success",
        "products_scraped": 20
      }
#### **curl**:
      curl -X POST http://127.0.0.1:8000/scrape/ \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer 1234" \
         -d '{"max_pages": 6}'

---

## **Customizing the Project**
### **Modify Storage Backend**
* Implement a new class inheriting from Storage and update the storage strategy in main.py.
### **Add New Notification Methods**
* Extend Notifier and include the new notifier in the composite notifier setup.
### **Update Token**
* Change the static token in the settings.py file.
---

## **Retry Mechanism**
* Configurable via max_retries and retry_delay parameters in the scraper function.
* Automatically retries on server errors (5xx) or timeouts.

