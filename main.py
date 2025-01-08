from data_src.create_tables import insert_voters, insert_candidates
from data_src.generate_data import generate_candidate_data, generate_voter_data
import psycopg2
from confluent_kafka import SerializingProducer
import simplejson as json
from data_src.connect_postgres import connect, cursor, get_candidates
from config import KAFKA_CONFIG, kafka_producer_config


candidates = get_candidates()

# Kafka Topics
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


if __name__ == "__main__":
    producer = SerializingProducer(kafka_producer_config)

    if len(candidates) == 0:
        for i in range(3): # 3 is number of candidate
            candidate = generate_candidate_data(i, 3) # 3 is number of candidate
            insert_candidates(connect, cursor, candidate)

    for i in range(1000): # 1000 is number of voters 
        voter_data = generate_voter_data()
        insert_voters(connect, cursor, voter_data)
        
        producer.produce(
            KAFKA_CONFIG["topic_voters"],# voters_topic
            key=voter_data["voter_id"],
            value=json.dumps(voter_data),   
            on_delivery=delivery_report
        )

        print('Produced voter {}, data: {}'.format(i, voter_data))
        producer.flush()


# create table in postgres
# create topic 
# data insert flow 
# note lại cách chạy -> tìm phương pháp tự động hoá khác 
# deploy src code on docker-compsoe 
# github action 
# tự động create user theo thời gian thực ví dụ mỗi 10s có 7-10 voters ! 
# format code !! 
        