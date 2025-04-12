import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    
def get_sql_alchemy_new_session():
    try:
        return SessionLocal()
    except Exception as e:
        print(f"Error: {e}")
        return None