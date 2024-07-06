from kafka_consumer import KafkaConsumer
from mongodb_client import MongoDBClient
from config import NEW_MONGODB_URI, NEW_MONGODB_DB_NAME, NEW_MONGODB_COLLECTION_NAME, NEW_KAFKA_TOPIC
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def is_b2b(description):
    prompt = f"Based on the following description, is this product likely a B2B or B2C offering?\n{description}"
    classification = model.generate_content(prompt)
    return "B2B" in classification.text.strip().upper()

def run_new_product_consumer():
    consumer = KafkaConsumer(NEW_KAFKA_TOPIC)
    mongodb_client = MongoDBClient(NEW_MONGODB_URI, NEW_MONGODB_DB_NAME, NEW_MONGODB_COLLECTION_NAME)

    print("Starting new product Kafka consumption and MongoDB writing...")

    try:
        for message in consumer.consume():
            data = json.loads(message)
            if is_b2b(data['description']):
                mongodb_client.insert_product(data['name'], data['description'])
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        mongodb_client.close()

    print("\nFinished consuming from new Kafka topic and writing to new MongoDB")