FROM python:3.9



# Set the working directory
WORKDIR /app
COPY requirements.txt .
# Copy the current directory contents into the container at /app


# Install any other necessary dependencies
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application's source code to the container
COPY . .
# Expose the necessary port
EXPOSE 8000

# Command to run the uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
