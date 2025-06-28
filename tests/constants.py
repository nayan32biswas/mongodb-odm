import os

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb://localhost:27017/testdb?directConnection=true&replicaSet=rs0",
)

CONNECTION_POOL_PARAMS = {
    "maxPoolSize": 10,
    "minPoolSize": 1,
    "maxIdleTimeMS": 30000,
}
