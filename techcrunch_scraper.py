from scraper_utils import setup_driver
from kafka_producer import KafkaProducer
from config import KAFKA_TOPIC_MISC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def scrape_techcrunch():
    driver = setup_driver()
    kafka_producer = KafkaProducer()
    
    urls = [
        "https://search.techcrunch.com/search;_ylc=X3IDMgRncHJpZANZZ1dnaThqQlNlaWNiZ3VnYmtTNDBBBG5fc3VnZwMwBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMzBHF1ZXJ5A2IyYgR0X3N0bXADMTcxMjgyODgyNA--?p=b2b&fr=techcrunch",
        "https://search.techcrunch.com/search;_ylt=Awrg1bB8vxdmwMIFHLunBWVH;_ylc=X1MDMTE5NzgwMjkxOQRfcgMyBGZyA3RlY2hjcnVuY2gEZ3ByaWQDSkV4MFphWXpSVi5fRHBfSnhpVS53QQRuX3JzbHQDMARuX3N1Z2cDOARvcmlnaW4Dc2VhcmNoLnRlY2hjcnVuY2guY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAM4BHF1ZXJ5A2J1c2luZXNzBHRfc3RtcAMxNzEyODMyMzkz?p=business&fr2=sb-top&fr=techcrunch"
    ]

    for url in urls:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        elements = driver.find_elements(By.CLASS_NAME, "fz-20")

        for element in elements:
            href = element.get_attribute("href")
            driver.get(href)

            h1_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "article__title")))
            p_element = wait.until(EC.presence_of_element_located((By.ID, "speakable-summary")))

            title = h1_element.text
            summary = p_element.text

            kafka_producer.produce(KAFKA_TOPIC_MISC, {
                'title': title,
                'content': summary
            })

    driver.quit()
    kafka_producer.flush()