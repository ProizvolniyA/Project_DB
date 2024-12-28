import model
import sessions
from fastapi import FastAPI, HTTPException, status
from fastapi import Query
from random import randint, uniform
from faker import Faker

def create_BD():
    engine = sessions.connect_to_base()
    model.BASE.metadata.create_all(engine)

if __name__ == "__main__":
    create_BD()

APP = FastAPI()
SESSION = sessions.connect_to_session()
