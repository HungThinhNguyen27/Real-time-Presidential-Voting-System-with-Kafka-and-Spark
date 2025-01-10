from data_src.create_tables import insert_voters, insert_candidates, create_tables
from data_src.generate_data import create_candidate_data, generate_voter_data, trump_data, harris_data
import psycopg2
from confluent_kafka import SerializingProducer
import simplejson as json
from data_src.connect_postgres import connect, cursor, get_candidates
from config import KAFKA_CONFIG, kafka_producer_config




# Kafka Topics
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


if __name__ == "__main__":
    producer = SerializingProducer(kafka_producer_config)
    create_tables(connect, cursor)
    candidates = get_candidates()
    print(len(candidates))
    if len(candidates) == 0:
        trump_candidate = create_candidate_data(trump_data) # 3 is number of candidate
        print(trump_data)
        harris_candidate = create_candidate_data(harris_data) # 3 is number of candidate
        print(trump_data)
        insert_candidates(connect, cursor, trump_candidate)
        insert_candidates(connect, cursor, harris_candidate)



    for i in range(156000000): # 1000 is number of voters 
        voter_data = generate_voter_data()
        print("voter_data", voter_data)
        insert_voters(connect, cursor, voter_data)
        
        producer.produce(
            KAFKA_CONFIG["topic_voters"],# voters_topic
            key=voter_data["voter_id"],
            value=json.dumps(voter_data),   
            on_delivery=delivery_report
        )

        print('Produced voter {}, data: {}'.format(i, voter_data))
        producer.flush()

# kafka-topics --list --bootstrap-server broker:29092
# kafka-console-consumer --topic topic_voters --bootstrap-server broker:9092 --from-beginning
# kafka-topics --delete --topic vehicle_data --bootstrap-server broker:29092        
# kafka-topics --delete --topic gps_data --bootstrap-server broker:29092        
# kafka-topics --delete --topic traffic_data --bootstrap-server broker:29092        
# kafka-topics --delete --topic weather_data --bootstrap-server broker:29092        
# kafka-topics --delete --topic emergency_data --bootstrap-server broker:29092        


# create table in postgres
# create topic 
# data insert flow 
# note lại cách chạy -> tìm phương pháp tự động hoá khác 
# deploy src code on docker-compsoe 
# github action 
# tự động create user theo thời gian thực ví dụ mỗi 10s có 7-10 voters ! 
# format code !! 
# hệ thống check xem có nhận được các phiếu vote hay chưa !!
        
"""
156tr người bầu cử/50 bang  -> viết src code giống với hệ thống bầu cử nước mỹ 
tổng phiếu cử tri là 538/50 bang 
tỉ lệ phiếu cử tri của từng bang phải theo thực tế!!!

ứng cử viên nào đạt 270 phiếu -> thắng 

show dashboard :
    - người đang dẫn đầu 
        + số phiếu cử tri đang dẫn theo thời gian thực 
        + số người bầu cử cho ứng viên !!
    - view MAP USA từng bang bầu cử -> xanh cho bà harris , đỏ cho ông trump 
        -> số phiếu cử tri trên từng bang 
    - ......

"""
