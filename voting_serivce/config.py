
# user generate


POSTGRES_CONFIG = {
    "host": "postgres", # container name of postgres_services on docker ! 
    "dbname": "voting",
    "user": "postgres",
    "password": "postgres"
}

# KAFKA CONFIG


KAFKA_CONFIG = {
    'topic': 'topic_votes',
    'broker_address': 'broker:29092' # kafka service on docker 
}

kafka_producer_config = {'bootstrap.servers': KAFKA_CONFIG["broker_address"]}