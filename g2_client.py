import requests
import time
import json
from config import API_ENDPOINT, API_KEY, KAFKA_TOPIC_API
from kafka_producer import KafkaProducer

def fetch_and_produce_products(producer):
    headers = {
        "Authorization": f"Token token={API_KEY}",
        "Content-Type": "application/vnd.api+json"
    }
    url = API_ENDPOINT

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            producer.produce(KAFKA_TOPIC_API, value=json.dumps(data))
            print("Produced data to Kafka topic")

            links = data.get("links", {})
            url = links.get("next")

        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

        if response.headers.get('X-RateLimit-Limit') and int(response.headers['X-RateLimit-Limit']) <= 100:
            print("Rate limit close to being exceeded. Sleeping for 1 second to ensure compliance...")
            time.sleep(1)