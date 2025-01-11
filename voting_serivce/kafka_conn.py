from config import kafka_producer_config
from confluent_kafka import Consumer, SerializingProducer
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
        topic,
        key=data["voter_id"],
        value=json.dumps(data),
        on_delivery=delivery_report
    )
    producer.poll(0)

consumer = Consumer(kafka_producer_config | {
    'group.id': 'voting-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})