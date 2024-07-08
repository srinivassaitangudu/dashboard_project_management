import psycopg2
import psycopg2.extras
import os

def get_db_conn():
    
    conn = psycopg2.connect(
        # dbname=os.getenv("DB_NAME"),
        dbname="hughesservicedelivery",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv('DB_PORT')
    )
    return conn