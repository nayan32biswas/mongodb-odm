python -m pip install --upgrade pip
python -m pip install "poetry==1.4.1"
python -m pip install "poetry-core==1.5.2"
python -m poetry install

if [ "$(docker ps -q -f name=mongo)" ]; then
    echo "Stopping my-mongodb-container..."
    docker stop my-mongodb-container
fi

docker run -d --rm --name mongo -p 27017:27017 mongo
poetry run scripts/test.sh
docker stop mongo
