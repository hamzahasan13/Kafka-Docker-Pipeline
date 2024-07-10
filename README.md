# Real-Time Data Pipeline with Kafka and Docker
This project demonstrates the setup of a real-time data pipeline using Kafka and Docker. The pipeline ingests streaming data, processes it in real-time using a Kafka consumer implemented in Python, and stores the processed data into a new Kafka topic.

## Project Setup
1. Prerequisites

* Docker installed on your machine (Docker Installation Guide) [https://www.docker.com/]
* Python 3.9+ installed (Python Installation Guide) [https://www.python.org/downloads/]

### Setting Up Development Environment

1. **Open VS Code and a New Terminal**.

2. **Clone this repository**:
    ```bash
    git clone https://github.com/hamzahasan13/Kafka-Docker-Pipeline.git
    cd Kafka-Docker-Pipeline
    ```

3. **Run Docker**.

4. **Create a virtual environment and activate it** (Replace `<env_name>` with your virtual environment name):
    ```bash
    python -m venv <env_name>
    source <env_name>/bin/activate
    ```

5. **Run Setup.sh to set dependencies and install libraries**:
    ```bash
    chmod +x setup.sh  # Make setup.sh executable
    ./setup.sh         # Install dependencies/libraries
    ```

6. **Run Docker compose in the terminal**:
    ```bash
    docker-compose up
    ```

7. **Wait until you get the similar output after running docker-compose**:
    ```css
    my-python-producer-1 | Produced message: {"user_id": "5ec2d697-3b93-4626-b8dc-28a9224a4f44", "app_version": "2.3.0", "ip": "149.144.104.36", "locale": "PA", "device_id": "70d46930-4dbf-4458-b100-179cd9ad90aa", "timestamp": 1720622216, "device_type": "android"}
    ```

8. **Once this similar message is received**, open a new terminal and run the following commands in this order:
    ```bash
    cd Kafka-Docker-Pipeline
    source <env_name>/bin/activate
    python src/logger.py
    python src/exeption.py
    python src/components/kafka_consumer.py
    ```

    This will start the Kafka consumer that processes messages from the `user-login` topic, aggregates data, and publishes processed data to `processed-user-login`.

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

## Testing and Validation

- Recommend testing procedures to validate the pipeline's functionality, including unit tests for individual components and integration tests for end-to-end scenarios.
- Consider load testing to assess scalability under various conditions.

## Deployment Considerations

- Provide guidance on deploying the pipeline to production environments, including scaling strategies and monitoring practices.
- Document backup and recovery procedures for Kafka topics and consumer state.

## Contributing

- Contributions are welcome! Fork the repository, create a branch, make your changes, and submit a pull request.

## License

- This project is licensed under the MIT License - see the LICENSE file for details.

