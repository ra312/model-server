# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app
COPY . .

# Install the required packages
RUN apt-get update && \
    apt-get install -y gcc && \
    pip install poetry==1.3.2 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Expose port 8000 to the outside world
EXPOSE 8000

# Start the FastAPI application using Uvicorn server
CMD ["poetry", "run", "uvicorn", "src/model_server/server.py:InferenceServer.app", "--host", "0.0.0.0", "--port", "8000"]