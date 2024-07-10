from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
import json

## Configuring Kafka Consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

## Configuring Kafka Producer
producer_conf = {
    'bootstrap.servers': 'localhost:29092'
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe(['user-login'])
output_topic = 'processed-user-login'

output_file = 'processed_user_login_data.json'

try:
    with open(output_file, 'w') as f:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            data = json.loads(msg.value().decode('utf-8'))
            json.dump(data, f)
            f.write('\n')
            
except KeyboardInterrupt:
    pass

finally:
    consumer.close()
