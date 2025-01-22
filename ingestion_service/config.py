
# user generate
RẠNDOMUSER_URL = 'https://randomuser.me/api/?nat=US'

NUMBER_OF_VOTERS = 156000000

POSTGRES_CONFIG = {
    "host": "postgres", # container name of postgres_services on docker ! 
    "dbname": "voting",
    "user": "postgres",
    "password": "postgres"
}

# KAFKA CONFIG


KAFKA_CONFIG = {
    'topic_voters': 'topic_voters',
    'broker_address': 'broker:29092' # kafka on docker 
}

kafka_producer_config = {'bootstrap.servers': KAFKA_CONFIG["broker_address"]}