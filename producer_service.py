from g2_client import fetch_and_produce_products
from kafka_producer import KafkaProducer

def run_producer_service():
    producer = KafkaProducer()
    print("Starting product extraction and Kafka production...")
    
    fetch_and_produce_products(producer)

    producer.flush()
    print("\nFinished producing to Kafka")
