from kafka_consumer import KafkaConsumer
from mongodb_client import MongoDBClient
import json
import google.generativeai as genai
from dotenv import load_dotenv
from config import KAFKA_CONFIG, KAFKA_TOPIC_API, KAFKA_TOPIC_BETALIST, KAFKA_TOPIC_MISC, GOOGLE_API_KEY, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME, MONGODB_URI
load_dotenv()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def is_b2b(description):
    prompt = f"Based on the following description, is this product likely a B2B or B2C offering?\n{description}"
    classification = model.generate_content(prompt)
    return "B2B" in classification.text.strip().upper()

def extract_product_info(title, content):
    prompt = f"Extract the product name and provide a brief description based on the following post:\nTitle: {title}\nContent: {content}\nIf no product is mentioned, return 'None' for both fields."
    response = model.generate_content(prompt)
    if response.parts:
        result = response.parts[0].text.strip().split('\n')
        if len(result) >= 2:
            return result[0], result[1]
    return 'None', 'None'

def run_consumer_service():
    consumers = [
        KafkaConsumer(KAFKA_TOPIC_API),
        KafkaConsumer(KAFKA_TOPIC_BETALIST),
        KafkaConsumer(KAFKA_TOPIC_MISC)
    ]
    mongodb_client = MongoDBClient(MONGODB_URI, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME)

    print("Starting Kafka consumption and MongoDB writing...")
    
    try:
        for consumer in consumers:
            for message in consumer.consume():
                data = json.loads(message)
                
                if consumer.topic == KAFKA_TOPIC_API:
                    # Process API data
                    for product_data in data.get("data", []):
                        name = product_data.get("attributes", {}).get("name")
                        description = product_data.get("attributes", {}).get("description")
                        if name and is_b2b(description):
                            mongodb_client.insert_product(name, description)
                
                elif consumer.topic == KAFKA_TOPIC_BETALIST:
                    # Process Betalist data
                    name = data.get('name')
                    description = data.get('description')
                    if name and is_b2b(description):
                        mongodb_client.insert_product(name, description)
                
                elif consumer.topic == KAFKA_TOPIC_MISC:
                    # Process Reddit, TechCrunch, ProductHunt data
                    title = data.get('title')
                    content = data.get('content')
                    if is_b2b(content):
                        product_name, product_description = extract_product_info(title, content)
                        if product_name != 'None':
                            mongodb_client.insert_product(product_name, product_description)

    except KeyboardInterrupt:
        pass
    finally:
        for consumer in consumers:
            consumer.close()
        mongodb_client.close()

    print("\nFinished consuming from Kafka and writing to MongoDB")
