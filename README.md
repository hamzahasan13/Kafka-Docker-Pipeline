# Real-Time Data Pipeline with Kafka and Docker
This project demonstrates the setup of a real-time data pipeline using Kafka and Docker. The pipeline ingests streaming data, processes it in real-time using a Kafka consumer implemented in Python, and stores the processed data into a new Kafka topic.

## Project Setup
Prerequisites

* Docker installed on your machine (Docker Installation Guide) [https://www.docker.com/]
* Python 3.9+ installed (Python Installation Guide) [https://www.python.org/downloads/]

### Setting Up Development Environment

1. **Open VS Code and a New Terminal**.

2. **Clone this repository**:
    ```bash
    git clone https://github.com/hamzahasan13/Kafka-Docker-Pipeline.git
    ```
    ```bash
    cd Kafka-Docker-Pipeline
    ```

3. **Run Docker in the background**.

4. **Create a virtual environment and activate it** (Replace `<env_name>` with your virtual environment name):
    ```bash
    python -m venv <env_name>
    ```
    ```bash
    source <env_name>/bin/activate
    ```

5. **Run Setup.sh to set dependencies and install libraries**:
    ### Makes setup.sh executable
   ```bash
    chmod +x setup.sh
    ```
   ### Installs dependencies/libraries
    ```bash
    ./setup.sh
    ```

7. **Start Docker and run Docker compose by executing in terminal**:
   ### For Docker version: 4.32.0 use the following command
    ```bash
    docker compose up
    ```
    ### For older Docker versions use the following command
   ```bash
    docker-compose up
    ```

9. **Wait until you get the similar output after running docker-compose**:
    ```css
    my-python-producer-1 | Produced message: {"user_id": "5ec2d697-3b93-xxxx-xxxx", "app_version": "2.3.0", "ip": "149.144.xxx.xxx", "locale": "PA", "device_id": "70d46930-4dbf-xxxx-xxxx", "timestamp": 1720622216, "device_type": "android"}
    ```

10. **Once this similar message is received**, open a new terminal and run the following commands in this order:
    ```bash
    cd Kafka-Docker-Pipeline
    ```
    ```bash
    source <env_name>/bin/activate
    ```
    ```bash
    python src/logger.py
    ```
    ```bash
    python src/exception.py
    ```
    ```bash
    python src/components/kafka_consumer.py
    ```

    This will activate environment for new terminal, set up error-handling and start the Kafka consumer that processes messages from the `user-login` topic, aggregates data, and publishes processed data to `processed-user-login`. The data after ingestion and aggregation is stored in "aggregated_data.json".

## Design Choices

- **Docker Compose**: Simplifies the setup of the development environment by orchestrating Kafka and Zookeeper containers.
- **Kafka**: Chosen for its robustness and ability to handle real-time data streaming with high throughput and low latency.
- **Python**: Utilized for its simplicity and powerful Kafka libraries (confluent-kafka) for building Kafka consumers and producers.

## Data Flow

### Data Generation

- Data is produced to the `user-login` Kafka topic.

### Kafka Consumer

- Reads messages from the `user-login` topic.
- Validates and processes JSON messages for required fields (`device_type`, `locale`, `timestamp`).
- Aggregates data:
  - Counts logins by device type (`device_type_counts`).
  - Counts logins by locale (`locale_counts`).
  - Tracks logins over time (`login_counts`).
- Performs anomaly detection based on login counts exceeding a threshold (`ANOMALY_THRESHOLD`).
- Publishes processed data to the `processed-user-login` topic.

## Ensuring Efficiency, Scalability, and Fault Tolerance

- **Efficiency**: The Kafka consumer polls for messages at a defined interval (`poll(1.0)`), optimizing resource usage and minimizing latency.
- **Scalability**: Kafka's partitioning mechanism allows for horizontal scaling by distributing data across multiple consumer instances.
- **Fault Tolerance**: Kafka ensures fault tolerance through replication of data across brokers (`bootstrap.servers`). Consumers use consumer groups (`group.id`) for load balancing and failover handling.

## Additional Questions

1. **How would you deploy this application in production?**

   Deploying the Kafka-Docker-Pipeline in a production environment involves several key steps to ensure it runs smoothly and reliably:
   
   - **Containerization with Docker**: Continue using Docker for production deployment to maintain consistency across different environments.
   - **Orchestration with Kubernetes**: Kubernetes is ideal for orchestrating containers in a production setting, providing features such as automatic scaling and self-healing.
   - **Ensuring High Availability**: Deploy Kafka with multiple brokers for fault tolerance and data redundancy.
   - **Monitoring and Logging**: Implement robust monitoring and logging with tools like Prometheus and Grafana.
   - **Security Considerations**: Secure Kafka with encryption and authentication mechanisms.
   - **CI/CD Pipeline**: Implement continuous integration and deployment pipelines for automated updates.
   
2. **What other components would you want to add to make this production ready?**

   To ensure our pipeline is production-ready, several components and practices can be that would be beneficial:
   
   - **Data Validation and Error Handling**: Enhance data validation mechanisms to handle edge cases and errors gracefully.
   - **Performance Optimization**: Fine-tune Kafka consumer configurations for optimal performance under varying loads.
   - **Scalability Planning**: Plan for scaling Kafka consumers and producers based on traffic patterns and data growth.
   - **Backup and Recovery**: Implement mechanisms for backing up Kafka topics and restoring data in case of failures.
   - **Monitoring and Alerting**: Set up comprehensive monitoring to track pipeline health, performance metrics, and anomalies.
   
3. **How can this application scale with a growing dataset?**

   To incorporate growing dataset, the application can be scaled effectively by leveraging Kafka's partitioning and consumer group capabilities:
   
   - **Horizontal Scaling**: Kafka allows multiple consumers (instances of Kafka consumer) to process messages in parallel by assigning partitions of a topic to different consumer instances. This horizontal scaling ensures that our application can handle increased message throughput as the dataset grows.
   
   - **Partitioning Strategy**: Implement an effective partitioning strategy for Kafka topics based on key attributes (e.g., user_id) to distribute data evenly across partitions. This strategy prevents hotspots and optimizes data processing.
   
   - **Consumer Group Management**: Utilize Kafka consumer groups to achieve load balancing and fault tolerance. Each consumer within a group processes a subset of partitions, enabling the application to scale by adding more consumers as needed without disrupting existing operations.
   
   - **Monitoring and Optimization**: Regularly monitor Kafka cluster performance, consumer lag, and resource utilization. Optimize configurations such as batch sizes, poll intervals, and concurrency to ensure efficient handling of large volumes of data.
   
## Contributing

- Contributions are welcome! Fork the repository, create a branch, make your changes, and submit a pull request.

## License

- This project is licensed under the MIT License - see the LICENSE file for details.

