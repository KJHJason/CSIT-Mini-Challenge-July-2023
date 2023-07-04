import motor.motor_asyncio as mongodb
from pymongo.database import Database

def get_db_client() -> Database:
    client = mongodb.AsyncIOMotorClient("mongodb+srv://userReadOnly:7ZT817O8ejDfhnBM@minichallenge.q4nve1r.mongodb.net/")
    return client["minichallenge"]
