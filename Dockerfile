# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app
COPY artifacts/rate_venues.pickle /app/rate_venues.pickle

# Install the required packages
RUN apt-get update && \
    apt-get install -y gcc && \
    python3 -m pip install recommendation-model-server

# Expose port 8000 to the outside world
EXPOSE 8000

# Start the FastAPI application using Uvicorn server

ENTRYPOINT [ "python3", "-m", \
    "recommendation_model_server", "--host", "0.0.0.0", "--port", "8000", \
    "--recommendation-model-path", "/app/rate_venues.pickle"]
