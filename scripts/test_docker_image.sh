#!/bin/bash


docker build -t my-fastapi-app .
# Run the Docker container in detached mode
docker run -d --name my-fastapi-app -p 8000:8000 my-fastapi-app

# Wait for the container to start
sleep 5

# Make a request to the API
curl -X 'POST' \
'http://0.0.0.0:8000/predict' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '[
  {
    "venue_id": -4202398962129790000,
    "conversions_per_impression": 0.3556765815,
    "price_range": 1,
    "rating": 8.6,
    "popularity": 4.4884057024,
    "retention_rate": 8.6,
    "session_id_hashed": 3352618370338455600,
    "position_in_list": 31,
    "is_from_order_again": 0,
    "is_recommended": 0
  }
]'

# Stop and remove the container

echo "stopped the container"
docker stop my-fastapi-app

echo "removed the container"
docker rm my-fastapi-app
