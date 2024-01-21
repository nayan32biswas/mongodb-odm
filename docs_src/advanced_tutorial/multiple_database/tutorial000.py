import os
from typing import Optional

from mongodb_odm import Document, apply_indexes, connect


class Log(Document):
    message: Optional[str] = None

    class ODMConfig:
        database = "logging"


def configuration():
    connect(
        os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"),
        databases={"logging"},
    )
    apply_indexes()


def create_data():
    _ = Log(message="Testing database log").create()


def retrieve_log():
    for log in Log.find():
        print(log)
    print()


def update_log():
    log = Log.find_one()
    if log:
        log.message = "Update log message"
        log.update()


def main():
    configuration()

    create_data()
    retrieve_log()
    update_log()


if __name__ == "__main__":
    main()
