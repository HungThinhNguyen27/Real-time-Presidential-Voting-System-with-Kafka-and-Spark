from config import KAFKA_CONFIG, kafka_producer_config
from confluent_kafka import SerializingProducer
import simplejson as json



producer = SerializingProducer(kafka_producer_config)

# Kafka Topics
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def kafka_producer(topic, data): 
    producer.produce(
    topic,# voters_topic
    key=data["voter_id"],
    value=json.dumps(data),   
    on_delivery=delivery_report
    )
    producer.flush()
