from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from kafka_producer import KafkaProducer
from config import KAFKA_TOPIC_BETALIST

def scrape_betalist(urls):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    kafka_producer = KafkaProducer()

    for url in urls:
        driver.get(url)
        time.sleep(5)

        products_count = 0
        while products_count < 10:
            driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(2)

            startup_cards = driver.find_elements(By.CLASS_NAME, "startupCard")
            for card in startup_cards:
                product_element = card.find_element(By.XPATH, ".//a[@class='block whitespace-nowrap text-ellipsis overflow-hidden font-medium']")
                product_name = product_element.text

                description_element = card.find_element(By.XPATH, ".//a[@class='block text-gray-500 dark:text-gray-400']")
                description = description_element.text

                kafka_producer.produce(KAFKA_TOPIC_BETALIST, {'name': product_name, 'description': description})
                products_count += 1

    driver.quit()
    kafka_producer.flush()