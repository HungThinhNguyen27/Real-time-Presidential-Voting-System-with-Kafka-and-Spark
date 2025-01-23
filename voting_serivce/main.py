import random
import time
import simplejson as json
from datetime import datetime, timedelta
from confluent_kafka import KafkaException, KafkaError
from config import KAFKA_CONFIG
from kafka_conn import consumer, kafka_producer
from db_operation.conn_db import insert_votes, get_candidates_json, connect, cursor


# Hàm tạo thời gian ngẫu nhiên trong khoảng thời gian nhất định
def random_datetime(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


# Khoảng thời gian cho voting_time
start_time = datetime(2024, 10, 1, 0, 0, 0)
end_time = datetime(2024, 11, 15, 23, 59, 59)

if __name__ == "__main__":

    candidates = get_candidates_json()
    candidates = [candidate[0] for candidate in candidates]
    if len(candidates) == 0:
        raise Exception("No candidates found in database")
    else:
        print(candidates)

    consumer.subscribe(["topic_voters"])  # topic_voters in kafka
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
                voter = json.loads(msg.value().decode("utf-8"))
                chosen_candidate = random.choice(candidates)
                vote = (
                    voter
                    | chosen_candidate
                    | {
                        "voting_time": random_datetime(start_time, end_time).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "vote": 1,
                    }
                )
                try:
                    print(
                        "User {} is voting for candidate: {}".format(
                            vote["voter_id"], vote["candidate_id"]
                        )
                    )
                    insert_votes(connect, cursor, vote)
                    kafka_producer(KAFKA_CONFIG["topic"], vote)

                except Exception as e:
                    print("Error: {}".format(e))
                    continue
            time.sleep(0.2)
    except KafkaException as e:
        print(e)
