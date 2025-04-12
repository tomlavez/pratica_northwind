import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        session = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        return session
    
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None