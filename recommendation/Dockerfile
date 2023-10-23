# Use an official Python runtime as the base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y build-essential

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

USER root

# Install FastAPI and Uvicorn (and any other dependencies)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Set the command to run the app using Uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Specify the listening port
EXPOSE 8000
