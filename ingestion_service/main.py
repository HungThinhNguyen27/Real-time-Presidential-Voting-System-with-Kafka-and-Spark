import psycopg2
import simplejson as json
from confluent_kafka import SerializingProducer
from kafka_conn import kafka_producer
from db_operation.connect_postgres import connect, cursor, get_candidates
from config import KAFKA_CONFIG, kafka_producer_config, NUMBER_OF_VOTERS
from db_operation.create_tables import insert_voters, insert_candidates, create_tables
from db_operation.generate_data import generate_voter_data, add_candidates, trump_data, harris_data

"""
create candidates and insert voters into postgres  

"""

if __name__ == "__main__":
    create_tables(connect, cursor)
    candidates = get_candidates()
    if len(candidates) == 0:
        candidate_list = add_candidates(trump_data, harris_data)
        for candidate in candidate_list:
            insert_candidates(connect, cursor, candidate)

    for i in range(NUMBER_OF_VOTERS): 

        voter_data = generate_voter_data()
        insert_voters(connect, cursor, voter_data)
        kafka_producer(KAFKA_CONFIG['topic_voters'], voter_data)
        print('Produced voter {}, data: {}'.format(i, voter_data))


# kafka-topics --list --bootstrap-server broker:29092
# kafka-console-consumer --topic topic_voters --bootstrap-server broker:9092 --from-beginning
# kafka-topics --delete --topic topic_votes --bootstrap-server broker:29092        
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
