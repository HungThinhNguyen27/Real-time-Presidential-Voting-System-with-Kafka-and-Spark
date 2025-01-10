from kafka import KafkaConsumer
from config import bootstrap_servers
import simplejson as json



# Function to create a Kafka consumer
def create_kafka_consumer(topic_name):
    # Set up a Kafka consumer with specified topic and configurations
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    return consumer


# Function to fetch data from Kafka
def fetch_data_from_kafka(consumer): # fix 
    # Poll Kafka consumer for messages within a timeout period
    messages = consumer.poll(timeout_ms=1000)
    data = []

    # Extract data from received messages
    for message in messages.values():
        for sub_message in message:
            data.append(sub_message.value)
    return data