from scraper_utils import setup_driver
from kafka_producer import KafkaProducer
from bs4 import BeautifulSoup
import time
from config import KAFKA_TOPIC_MISC

def scrape_producthunt():
    driver = setup_driver()
    kafka_producer = KafkaProducer()
    
    urls = [
        'https://www.producthunt.com/categories/work-productivity',
        'https://www.producthunt.com/categories/finance',
        'https://www.producthunt.com/categories/marketing-sales',
        'https://www.producthunt.com/categories/platforms',
        'https://www.producthunt.com/categories/web3',
        'https://www.producthunt.com/categories/ecommerce',
        'https://www.producthunt.com/categories/ai'
    ]

    for url in urls:
        driver.get(url)
        time.sleep(3)

        for _ in range(2):  # Scroll down multiple times to load more products
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_cards = soup.select('.flex.flex-col.pb-12 > div.mb-10')

        for card in product_cards[:10]:  # Extract only 10 products from each category
            title_element = card.select_one('div.flex.flex-row.items-center > a > div.text-18.font-semibold.text-blue')
            description_element = card.select_one('div.text-14.sm\\:text-16.font-normal.text-light-grey.mb-6')

            title = title_element.text.strip() if title_element else ''
            description = description_element.text.strip() if description_element else ''

            kafka_producer.produce(KAFKA_TOPIC_MISC, {
                'title': title,
                'content': description
            })

    driver.quit()
    kafka_producer.flush()