import psycopg2
import streamlit as st
from config import POSTGRES_CONFIG



connect = psycopg2.connect(
    host=POSTGRES_CONFIG["host"],
    dbname=POSTGRES_CONFIG["dbname"],
    user=POSTGRES_CONFIG["user"],
    password=POSTGRES_CONFIG["password"]    
)
cursor = connect.cursor()

@st.cache_data
def fetch_voting_stats(): # fix 
    # Connect to PostgreSQL database

    # Fetch total number of voters
    cursor.execute("""
        SELECT count(*) voters_count FROM voters
    """)
    voters_count = cursor.fetchone()[0]

    # Fetch total number of candidates
    cursor.execute("""
        SELECT count(*) candidates_count FROM candidates
    """)
    candidates_count = cursor.fetchone()[0]

    return voters_count, candidates_count