from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
import json
import logging
import os
import time
from datetime import datetime
from collections import defaultdict
from exception import CustomException
from logger import logging
import sys

# Kafka Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'my-group',
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

# Aggregation data structures
device_type_counts = defaultdict(int)
locale_counts = defaultdict(int)
login_counts = defaultdict(int)

# Anomaly detection threshold
ANOMALY_THRESHOLD = 10

def process_message(msg):
    try:
        data = json.loads(msg.value().decode('utf-8'))
        
        # Check for required keys
        if 'device_type' not in data or 'locale' not in data or 'timestamp' not in data:
            raise KeyError("Missing required keys in data")

        # Aggregation
        device_type_counts[data['device_type']] += 1
        locale_counts[data['locale']] += 1
        
        # Convert timestamp
        timestamp = datetime.fromtimestamp(data['timestamp'])
        login_counts[timestamp.strftime('%Y-%m-%d %H:%M')] += 1

        # Anomaly detection
        if login_counts[timestamp.strftime('%Y-%m-%d %H:%M')] > ANOMALY_THRESHOLD:
            logging.warning(f"Anomaly detected: High number of logins at {timestamp.strftime('%Y-%m-%d %H:%M')}")

        return data
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error processing message: {str(e)}")
        return None  # Return None or handle gracefully to continue processing

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
        if data is not None:
            producer.produce(output_topic, json.dumps(data).encode('utf-8'))
            producer.flush()
            
            # Log aggregation results
            logging.info(f"Real-time Aggregation:")
            logging.info(f"Logins by Device Type: {dict(device_type_counts)}")
            logging.info(f"Logins by Locale: {dict(locale_counts)}")
            logging.info(f"Logins Over Time: {dict(login_counts)}")
            
            # Save aggregated data to JSON file
            output_data = {
                "Logins by Device Type": dict(device_type_counts),
                "Logins by Locale": dict(locale_counts),
                "Logins Over Time": dict(login_counts)
            }
            
            output_file = 'aggregated_data.json'
            try:
                with open(output_file, 'w') as f:
                    json.dump(output_data, f, indent=4)
                logging.info(f"Aggregated data saved to {output_file}")
            except Exception as e:
                logging.error(f"Failed to save aggregated data to {output_file}: {str(e)}")
        
        time.sleep(5)  # Sleep to simulate real-time processing

except KeyboardInterrupt:
    logging.info("Shutting down consumer.")
except Exception as e:
    logging.exception("An error occurred during processing.")
    raise CustomException(e, sys)
finally:
    consumer.close()
    logging.info("Consumer closed.")
