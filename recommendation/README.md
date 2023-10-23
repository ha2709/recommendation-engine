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

## Run the Docker containers using

`docker-compose up -d.`

This setup will distribute the incoming traffic across the two instances of recommendation service, providing a basic load balancing mechanism. You can scale up the number of instances and fine-tune the load balancing configuration to suit specific requirements.

set up load balancing using HAProxy:

1. **Install HAProxy on your server if it's not already installed:**

```
sudo apt-get update
sudo apt-get install haproxy

```

2. **Configure the HAProxy settings:**

Edit the HAProxy configuration file, typically located at `/etc/haproxy/haproxy.cfg`.

`sudo nano /etc/haproxy/haproxy.cfg`

Add the following configuration to set up load balancing for two backend servers:

```
frontend myapp
    bind *:80
    mode http
    default_backend myapp

backend myapp
    mode http
    balance roundrobin
    option httpchk HEAD / HTTP/1.1\r\nHost:localhost
    server backend1 your_server_ip1:8000 check
    server backend2 your_server_ip2:8000 check

```

3. **Save the configuration file and restart HAProxy:**

`sudo service haproxy restart`

Make sure to replace your_server_ip1 and your_server_ip2 with the actual IP addresses of your backend servers.

With this configuration, HAProxy will balance the traffic between the two backend servers, providing high availability and ensuring that if one server goes down, the other server can handle the requests.

Additionally, you may need to configure your firewall settings to allow traffic on the appropriate ports (e.g., port 80) for HAProxy and your backend servers.
