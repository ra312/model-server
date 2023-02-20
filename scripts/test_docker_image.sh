#!/bin/bash


echo "Check if the Docker image already exists"
if [[ "$(docker images -q my-fastapi-app 2> /dev/null)" == "" ]]; then
    echo "Building Docker image"
    docker build -t my-fastapi-app .
fi

# Run the Docker container in detached mode
docker run -d --name my-fastapi-app -p 8000:8000 my-fastapi-app

# Wait for the container to start
sleep 5

# Make a request to the API
curl http://localhost:8000/predict

# Stop and remove the container
docker stop my-fastapi-app
docker rm my-fastapi-app
