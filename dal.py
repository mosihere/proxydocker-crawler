import os
from typing import List, Dict
from pymongo import MongoClient



def db_connection(database_name: str) -> MongoClient:
    """
    Get a single arg as database_name
    read database password from environment variables and returns a MongoClient Connection

    Args:
        database_name: str

    Returns
        MongoClient() Connection.
    """
    db_pass = os.environ.get('MONGODB_PASS')

    CONNECTION_STRING = f"mongodb+srv://mosihere:{db_pass}@mostafa.q0repad.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    return client[database_name]


def commit(data: List[Dict]) -> str:
    """
    Get a single arg as data
    Create a Database called MyDB
    Create a Collection named proxies
    finally insert data to proxies collection.

    Args:
        data: List[Dict]

    Returns
        Collection
    """
    # Create the database
    database = db_connection('MyDB')

    # Create the collection
    collection = database["proxies"]
    collection.insert_many(data)
