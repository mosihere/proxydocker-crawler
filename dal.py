from pymongo import MongoClient
import os


class CreateDataBase:
    """
    When instantiate Mongo Password will read from environment variables.
    Need a single argument as db_name.
    """

    def __init__(self) -> None:
        self.password = os.environ['MONGODB_PASS']

    def get_database(self, db_name: str) -> MongoClient:
        """
        Connect to Mongo and Create a database named "myDB"

        Returns:
            Created DataBase

        ReturnType: MongoClient
        """
        db_name = db_name

        CONNECTION_STRING = f"mongodb+srv://mosihere:{self.password}@mostafa.q0repad.mongodb.net/?retryWrites=true&w=majority"

        # Create a connection using MongoClient.
        client = MongoClient(CONNECTION_STRING)

        # Create the database
        return client[db_name]
