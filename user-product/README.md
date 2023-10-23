# Local Setup and Running Instructions

Before running the application, please follow the steps below:

## Stop mySQL on your local

To stop the mySQL service on your local machine, execute the following command:

`systemctl stop mysql`

## Running the Application with Docker Compose

To build and run the application using Docker Compose,in the user-product folder, use the following command:

`docker-compose up --build`

## Running the Application with Docker Compose

To run the application using Docker Compose, execute the command:

`docker-compose up`

## Running the Application Outside the Container

To run the application outside the container, use the following command:

`uvicorn main:app --reload`

## Database Migration

If there is no data in the database, you can migrate all datasets to the database by following these steps:

1. **Access the running container using the command:**

   `docker exec -it user-product /bin/bash`

2. **Run the migration script:**

   `python3 migration/migrate_all.py`

## Running Tests

To run the tests, execute the following command:

pytest
Sample API Request
You can use the following curl command to make a sample API request:

      ```
      curl -X 'GET' \
      'http://localhost:8001/api/v1/product' \
      -H 'accept: application/json' \
      -H 'access_token: supersecretkey'
      ```

Feel free to modify the instructions and commands based on your specific environment and requirements.
