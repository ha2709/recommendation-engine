# Recommendation Service

This project is a recommendation service that provides specific recommendations based on user input.

## Docker Image Build

To build the Docker image, use the following command:

`docker build -t recommendation .`

##Run Docker Container

To run the Docker container, execute the following command:

`docker run --network host recommendation`

## Access API Documentation

To access the API documentation, open your preferred web browser and navigate to:

`http://127.0.0.1:8000/docs`

## Make API Requests

You can use the following curl command to make an API request:

```
curl -X 'GET' \
'http://localhost:8000/api/v1/recommend/103' \
-H 'accept: application/json' \
-H 'access_token: supersecretkey'

```

## Local Development

For local development, use the following command:

`uvicorn main:app --reload --port 8000`

## Run Tests

To run the tests, use the command:

`pytest`

Feel free to modify and improve the service as needed.
