import random
import time
from datetime import datetime
import psycopg2
import simplejson as json
from confluent_kafka import Consumer, KafkaException, KafkaError, SerializingProducer
from main import delivery_report
from config import KAFKA_CONFIG, kafka_producer_config
from data_src.connect_postgres import connect, cursor, get_candidates_json
from data_src.create_tables import insert_votes


consumer = Consumer(kafka_producer_config | {
    'group.id': 'voting-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})

producer = SerializingProducer(kafka_producer_config)



if __name__ == "__main__":


    candidates = get_candidates_json()
    candidates = [candidate[0] for candidate in candidates]
    if len(candidates) == 0:
        raise Exception("No candidates found in database")
    else:
        print(candidates)

    consumer.subscribe(['topic_voters']) # topic_voters in kafka
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                break
            else:
                voter = json.loads(msg.value().decode('utf-8'))
                chosen_candidate = random.choice(candidates)
                vote = voter | chosen_candidate | {
                    "voting_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "vote": 1
                }
                try:
                    print("User {} is voting for candidate: {}".format(vote['voter_id'], vote['candidate_id']))
                    insert_votes(connect, cursor, vote)

                    producer.produce(
                        KAFKA_CONFIG["topic_votes"],
                        key=vote["voter_id"],
                        value=json.dumps(vote),
                        on_delivery=delivery_report
                    )
                    producer.poll(0)
                except Exception as e:
                    print("Error: {}".format(e))
                    # conn.rollback()
                    continue
            time.sleep(0.2)
    except KafkaException as e:
        print(e)