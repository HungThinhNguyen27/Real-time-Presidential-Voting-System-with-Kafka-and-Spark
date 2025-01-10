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

def get_candidates():
    cursor.execute("""
        SELECT * FROM candidates
    """)
    candidates = cursor.fetchall()
    return candidates

def get_candidates_json():

    cursor.execute("""
        SELECT row_to_json(t)
        FROM (
            SELECT * FROM candidates
        ) t;
    """)
    candidates = cursor.fetchall()
    return candidates

