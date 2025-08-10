#!/bin/bash

set -e
echo "Starting replica set initialization..."

# Wait for MongoDB instances to be ready for connections instead of fixed sleep
echo "Waiting for MongoDB instances to be ready..."
MONGO_READY_RETRIES=30
MONGO_READY_COUNT=0

# Wait for primary MongoDB to be ready
until mongosh --quiet --host mongodb:27017 --eval 'db.adminCommand("ping")' >/dev/null 2>&1; do
  MONGO_READY_COUNT=$((MONGO_READY_COUNT + 1))
  echo "Waiting for mongodb:27017 to be ready... Attempt $MONGO_READY_COUNT/$MONGO_READY_RETRIES"
  if [ $MONGO_READY_COUNT -ge $MONGO_READY_RETRIES ]; then
    echo "Timeout waiting for mongodb:27017 to be ready!" >&2
    exit 1
  fi
  sleep 0.5s
done

# Wait for follower MongoDB to be ready
MONGO_READY_COUNT=0
until mongosh --quiet --host mongodb_follower:27017 --eval 'db.adminCommand("ping")' >/dev/null 2>&1; do
  MONGO_READY_COUNT=$((MONGO_READY_COUNT + 1))
  echo "Waiting for mongodb_follower:27017 to be ready... Attempt $MONGO_READY_COUNT/$MONGO_READY_RETRIES"
  if [ $MONGO_READY_COUNT -ge $MONGO_READY_RETRIES ]; then
    echo "Timeout waiting for mongodb_follower:27017 to be ready!" >&2
    exit 1
  fi
  sleep 0.5s
done

echo "Both MongoDB instances are ready!"

echo "Checking if replica set is already initialized..."
# Check if replica set is already configured
if mongosh --quiet --host mongodb:27017 --eval 'try { rs.status(); print("ALREADY_INITIALIZED"); } catch(e) { if (e.code === 94) print("NOT_INITIALIZED"); else throw e; }' | grep -q "ALREADY_INITIALIZED"; then
  echo "Replica set is already initialized, skipping rs.initiate()"
else
  echo "Initiating replica set..."
  mongosh --host mongodb:27017 --eval '
    rs.initiate({
      _id: "rs0",
      members: [
        { _id: 0, host: "mongodb:27017", priority: 5 },
        { _id: 1, host: "mongodb_follower:27017", priority: 1 }
      ]
    })
  '
  echo "Replica set initialization command completed"
fi

echo "Waiting for PRIMARY election..."
RETRIES=30
COUNT=0

# First wait for primary to be elected - using multiple methods to check
until mongosh --quiet --host mongodb:27017 --eval '
  try {
    var hello = db.hello();
    var isMaster = db.isMaster();
    if (hello.isWritablePrimary === true || hello.ismaster === true || isMaster.ismaster === true) {
      print("PRIMARY_READY");
    } else {
      print("NOT_PRIMARY: " + JSON.stringify({hello: hello, isMaster: isMaster}));
    }
  } catch(e) {
    print("ERROR_CHECKING: " + e.message);
  }
' | grep -q "PRIMARY_READY"; do
  COUNT=$((COUNT + 1))
  echo "Waiting for MongoDB PRIMARY election... Attempt $COUNT/$RETRIES"

  # Debug: show what we're getting
  if [ $COUNT -eq 1 ] || [ $((COUNT % 5)) -eq 0 ]; then
    echo "Debug - Current status:"
    mongosh --quiet --host mongodb:27017 --eval '
      try {
        var hello = db.hello();
        var isMaster = db.isMaster();
        print("hello.isWritablePrimary: " + hello.isWritablePrimary);
        print("hello.ismaster: " + hello.ismaster);
        print("isMaster.ismaster: " + isMaster.ismaster);
        print("hello.me: " + hello.me);
        print("hello.primary: " + hello.primary);
      } catch(e) {
        print("Debug error: " + e.message);
      }
    ' || echo "Failed to get debug info"
  fi

  if [ $COUNT -ge $RETRIES ]; then
    echo "Timed out waiting for MongoDB PRIMARY election!" >&2
    echo "Current replica set status:"
    mongosh --quiet --host mongodb:27017 --eval 'printjson(rs.status())' || echo "Failed to get replica set status"
    exit 1
  fi
  sleep 1s
done

echo "PRIMARY elected! Now verifying it's ready for writes..."

# Additional verification: ensure the primary can actually handle writes
WRITE_RETRIES=15
WRITE_COUNT=0
until mongosh --quiet --host mongodb:27017 --eval '
  try {
    db.test_init.insertOne({test: "write_check", timestamp: new Date()});
    db.test_init.deleteMany({test: "write_check"});
    print("WRITE_SUCCESS");
  } catch(e) {
    print("WRITE_FAILED: " + e.message);
  }
' | grep -q "WRITE_SUCCESS"; do
  WRITE_COUNT=$((WRITE_COUNT + 1))
  echo "Waiting for PRIMARY to be ready for writes... Attempt $WRITE_COUNT/$WRITE_RETRIES"
  if [ $WRITE_COUNT -ge $WRITE_RETRIES ]; then
    echo "Timed out waiting for MongoDB PRIMARY to accept writes!" >&2
    echo "Current replica set status:"
    mongosh --quiet --host mongodb:27017 --eval 'printjson(rs.status())' || echo "Failed to get replica set status"
    exit 1
  fi
  sleep 1s
done

echo "MongoDB PRIMARY is ready!"
echo "Final replica set status verification:"
mongosh --quiet --host mongodb:27017 --eval 'printjson(rs.status())'
echo "Replica set initialization completed successfully."
