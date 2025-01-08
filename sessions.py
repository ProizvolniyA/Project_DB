from dotenv import load_dotenv
import os
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker

load_dotenv()
def connect_to_base() -> sql.Engine:
    session_url = sql.engine.URL.create(
        drivername="postgresql+pg8000",
        username=os.getenv("BASE_USER"),  # os["POSTGRES_USER"]
        password=os.getenv("BASE_PASSWORD"),
        host=os.getenv("BASE_HOST"),
        port=os.getenv("BASE_PORT"),
        database=os.getenv("BASE_DB")
    )
    return sql.create_engine(session_url)  # return engine

def connect_to_session():
    engine = connect_to_base()
    Session = sessionmaker(bind=engine)
    return Session()
