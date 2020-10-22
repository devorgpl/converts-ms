import os

from pymongo import MongoClient

DB_HOST = os.environ.get("DB_HOST", 'localhost')


def converts_collection():
    client = MongoClient(DB_HOST, 27017)
    db = client['companyms']
    collection = db['companies']
    return collection
