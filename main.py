from g2_client import fetch_and_produce_products
from betalist_scraper import scrape_betalist
from reddit_scraper import scrape_reddit
from techcrunch_scraper import scrape_techcrunch
from producthunt_scraper import scrape_producthunt
from consumer_service import run_consumer_service
from kafka_producer import KafkaProducer
from config import KAFKA_TOPIC_API
import threading

def run_g2_producer():
    g2_producer = KafkaProducer()
    fetch_and_produce_products(g2_producer)

def run_other_scrapers():
    betalist_urls = [
        "https://betalist.com/markets/saas",
        "https://betalist.com/markets/artificial-intelligence",
        "https://betalist.com/markets/productivity"
    ]
    scrape_betalist(betalist_urls)
    scrape_reddit(['startup', 'entrepreneur', 'SaaS'])
    scrape_techcrunch()
    scrape_producthunt()

if __name__ == "__main__":
    # Start G2 producer in a separate thread
    g2_thread = threading.Thread(target=run_g2_producer)
    g2_thread.start()

    # Start other scrapers in a separate thread
    scrapers_thread = threading.Thread(target=run_other_scrapers)
    scrapers_thread.start()

    # Start consumer service
    consumer_thread = threading.Thread(target=run_consumer_service)
    consumer_thread.start()

    # Wait for all threads to complete
    g2_thread.join()
    scrapers_thread.join()
    consumer_thread.join()

    print("All processes completed.")