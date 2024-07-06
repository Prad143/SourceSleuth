from confluent_kafka import Consumer, KafkaError
from config import KAFKA_CONFIG

class KafkaConsumer:
    def __init__(self, topic):
        consumer_config = KAFKA_CONFIG.copy()
        consumer_config.update({
            'group.id': f'{topic}_consumer_group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer = Consumer(consumer_config)
        self.consumer.subscribe([topic])

    def consume(self):
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    break

            yield msg.value().decode('utf-8')

    def close(self):
        self.consumer.close()