# kafka_producer.py
from confluent_kafka import Producer
from config import KAFKA_CONFIG, KAFKA_TOPIC, NEW_KAFKA_TOPIC
import json

class KafkaProducer:
    def __init__(self):
        self.producer = Producer(KAFKA_CONFIG)

    def produce(self, topic, value):
        self.producer.produce(topic, value=json.dumps(value))

    def flush(self):
        self.producer.flush()