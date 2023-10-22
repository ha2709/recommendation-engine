# Recommendation Engine

## Scaling the Recommendation Engine Horizontally

To ensure the scalability and fault tolerance of the Recommendation Engine, the following strategies have been implemented:

1. **Microservices Architecture:** The Recommendation Engine has been divided into two separate microservices, the User-Product Service and the Recommendation Service, communicating via HTTP. This modular approach allows for independent scaling and development.

2. **Fallback Mechanism:** In the event of a failure in the User-Product Service, the Recommendation Service automatically retrieves data from the dataset.csv file to train the model and deliver results, ensuring continuous operation of the system.

3. **Horizontal Scaling with Load Balancer:** The system can scale horizontally by adding more nodes or resources, facilitated by a load balancer that evenly distributes incoming traffic among multiple instances of the Recommendation Service.

4. **Infrastructure Management with Terraform and Kubernetes:** Infrastructure provisioning and scaling are handled using Terraform, which allows for the creation of the necessary resources, while Kubernetes automates the scaling of instances based on current load and performance metrics.

5. **API-KEY Authentication:** Each request is authenticated using an API-KEY, enabling independent handling of each request without relying on previous requests.

6. **Caching and Asynchronous Processing:** Caching in memory is utilized to reduce the load on the database and improve response time. Asynchronous processing is employed to handle tasks in the background, allowing the system to quickly respond to requests.

Please refer to the project documentation for more detailed information on the system architecture and implementation details.
