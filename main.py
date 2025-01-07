from create_tables import create_tables, insert_voters
from generate_data import generate_candidate_data, generate_voter_data
import psycopg2
from confluent_kafka import SerializingProducer
import simplejson as json


BASE_URL = 'https://randomuser.me/api/?nat=gb'
PARTIES = ["Management Party", "Savior Party", "Tech Republic Party"]

# Kafka Topics
voters_topic = 'voters_topic'
candidates_topic = 'candidates_topic'

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


if __name__ == "__main__":
    producer = SerializingProducer({'bootstrap.servers': 'localhost:9092', })


    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()  
    create_tables(conn, cur)
    cur.execute("""
        SELECT * FROM candidates
    """)
    candidates = cur.fetchall()
    print(candidates)

    if len(candidates) == 0:
        for i in range(3):
            candidate = generate_candidate_data(i, 3)
            print(candidate)
            cur.execute("""
                        INSERT INTO candidates (candidate_id, candidate_name, party_affiliation, biography, campaign_platform, photo_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                candidate['candidate_id'], candidate['candidate_name'], candidate['party_affiliation'], candidate['biography'],
                candidate['campaign_platform'], candidate['photo_url']))
            conn.commit()

    for i in range(1000):
        voter_data = generate_voter_data()
        insert_voters(conn, cur, voter_data)
        
        producer.produce(
            voters_topic,
            key=voter_data["voter_id"],
            value=json.dumps(voter_data),
            on_delivery=delivery_report
        )

        print('Produced voter {}, data: {}'.format(i, voter_data))
        producer.flush()