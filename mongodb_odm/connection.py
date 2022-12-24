from pymongo import MongoClient
from pymongo.database import Database

__connection = {}


def _get_connection_client(url: str) -> MongoClient:
    return MongoClient(url)


def connect(url: str) -> MongoClient:
    if "client" in __connection:
        return __connection["client"]
    __connection["url"] = url
    __connection["client"] = _get_connection_client(url)
    return __connection["client"]


def disconnect() -> bool:
    if "client" in __connection:
        __connection["client"].close()
        del __connection["client"]
    return True


def force_disconnect() -> bool:
    disconnect()
    if "url" in __connection:
        del __connection["url"]
    return True


def get_client() -> MongoClient:
    if not __connection or "client" not in __connection:
        if "url" in __connection:
            connect(__connection["url"])
        else:
            raise Exception("DB connection is not provided")
    return __connection["client"]


def get_db() -> Database:
    return get_client().get_database()
