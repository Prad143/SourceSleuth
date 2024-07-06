from kafka_consumer import KafkaConsumer
from mongodb_client import MongoDBClient
from config import NEW_MONGODB_URI, NEW_MONGODB_DB_NAME, NEW_MONGODB_COLLECTION_NAME, NEW_KAFKA_TOPIC
import json

def run_new_consumer_service():
    consumer = KafkaConsumer(NEW_KAFKA_TOPIC)
    mongodb_client = MongoDBClient(NEW_MONGODB_URI, NEW_MONGODB_DB_NAME, NEW_MONGODB_COLLECTION_NAME)

    print("Starting new Kafka consumption and MongoDB writing...")
    
    try:
        for message in consumer.consume():
            data = json.loads(message)
            mongodb_client.insert_product(data['name'], data['description'])
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        mongodb_client.close()

    print("\nFinished consuming from new Kafka topic and writing to new MongoDB")