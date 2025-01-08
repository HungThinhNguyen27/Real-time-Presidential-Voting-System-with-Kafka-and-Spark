
# user generate
RẠNDOMUSER_URL = 'https://randomuser.me/api/?nat=gb'


POSTGRES_CONFIG = {
    "host": "localhost",
    "dbname": "voting",
    "user": "postgres",
    "password": "postgres"
}

# KAFKA CONFIG

KAFKA_CONFIG = {
    "topic_voters": "topic_voters",
    "topic_votes": "topic_voters",
    'broker_address': 'localhost:9092'
}

kafka_producer_config = {'bootstrap.servers': KAFKA_CONFIG["broker_address"]}