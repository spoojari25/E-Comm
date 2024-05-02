import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException,status


def get_connection():
    try:
        conn = psycopg2.connect(host='localhost',user='postgres',password = 'sudo@2521',
                         database='products',cursor_factory=RealDictCursor)
        print("Database connected successfully")
        return conn
    except Exception as error:
        raise error