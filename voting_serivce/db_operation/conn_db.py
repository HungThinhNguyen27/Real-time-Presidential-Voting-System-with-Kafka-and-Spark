import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import POSTGRES_CONFIG


# Correct way to use the POSTGRES_CONFIG dictionary to connect
connect = psycopg2.connect(
    host=POSTGRES_CONFIG["host"],
    dbname=POSTGRES_CONFIG["dbname"],
    user=POSTGRES_CONFIG["user"],
    password=POSTGRES_CONFIG["password"]    
)
cursor = connect.cursor()

def get_candidates_json():

    cursor.execute("""
        SELECT row_to_json(t)
        FROM (
            SELECT * FROM candidates
        ) t;
    """)
    candidates = cursor.fetchall()
    return candidates

def insert_votes(conn, cur, vote):
    cur.execute("""
            INSERT INTO votes (voter_id, candidate_id, voting_time)
            VALUES (%s, %s, %s)
        """, (vote['voter_id'], vote['candidate_id'], vote['voting_time']))

    conn.commit()


