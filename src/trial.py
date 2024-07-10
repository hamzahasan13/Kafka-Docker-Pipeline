from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
import json
from datetime import datetime
import pandas as pd
from collections import defaultdict
import time

# Kafka Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'processing-group',
    'auto.offset.reset': 'earliest'
}

# Kafka Producer configuration
producer_conf = {
    'bootstrap.servers': 'localhost:29092'
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe(['user-login'])
output_topic = 'processed-user-login'

# Initialize data structures for aggregation
device_type_counts = defaultdict(int)
locale_counts = defaultdict(int)

# Define a threshold for anomaly detection (e.g., more than 10 logins per minute)
anomaly_threshold = 10
login_counts = defaultdict(int)

def process_message(msg):
    # Parse the message
    data = json.loads(msg.value().decode('utf-8'))
    
    # Update device type and locale counts
    device_type_counts[data['device_type']] += 1
    locale_counts[data['locale']] += 1
    
    # Convert timestamp to datetime and update login counts
    login_time = datetime.fromtimestamp(data['timestamp'])
    minute_bucket = login_time.strftime('%Y-%m-%d %H:%M')
    login_counts[minute_bucket] += 1
    
    # Anomaly detection
    if login_counts[minute_bucket] > anomaly_threshold:
        print(f"Anomaly detected! More than {anomaly_threshold} logins in {minute_bucket}")
    
    # Return processed data
    return data

try:
    while True:
        msg = consumer.poll(1.0)  # Wait for a message for 1 second
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        
        data = process_message(msg)
        producer.produce(output_topic, json.dumps(data).encode('utf-8'))
        producer.flush()
        
        # Print real-time aggregation results
        print("Real-time Aggregation:")
        print(f"Logins by Device Type: {dict(device_type_counts)}")
        print(f"Logins by Locale: {dict(locale_counts)}")
        print(f"Logins Over Time: {dict(login_counts)}")
        
        # Sleep for a bit to simulate real-time processing
        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
