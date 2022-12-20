from pymongo import MongoClient

_connection = {}


def _get_connection_client(url: str):
    return MongoClient(url)


def connect(url: str):
    if "client" in _connection:
        return _connection["client"]
    _connection["url"] = url
    _connection["client"] = _get_connection_client(url)
    return _connection["client"]


def disconnect():
    _connection["client"].close()
    del _connection["client"]


def get_client():
    if not _connection or "client" not in _connection:
        if "url" in _connection:
            connect(_connection["url"])
        else:
            raise Exception("DB connection is not provided")
    return _connection["client"]


def get_db():
    return get_client().get_database()
