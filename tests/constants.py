import os

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb://localhost:27017/testdb?replicaSet=rs0",
)

CONNECTION_POOL_PARAMS = {
    "maxPoolSize": 255,
    "minPoolSize": 1,
    "maxIdleTimeMS": 30000,
    "connectTimeoutMS": 5000,
    "socketTimeoutMS": 5000,
    "serverSelectionTimeoutMS": 5000,
    "readPreference": "primary",
}
