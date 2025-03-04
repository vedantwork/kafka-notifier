import asyncio
import json
import logging
import os
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv
from pydantic import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Kafka configurations
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC_NAME = os.getenv("TOPIC_NAME")

def ensure_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    try:
        metadata = admin_client.list_topics(timeout=10)
        if topic_name in metadata.topics:
            logging.info(f"Kafka topic '{topic_name}' already exists.")
            return
        logging.info(f"Kafka topic '{topic_name}' does not exist. Creating...")
        new_topic = NewTopic(
            topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        future = admin_client.create_topics([new_topic])
        for topic, f in future.items():
            try:
                f.result()
                logging.info(f"Kafka topic '{topic}' created successfully.")
            except Exception as e:
                logging.error(f"Failed to create topic '{topic}': {e}")
                raise RuntimeError(f"Error creating Kafka topic: {e}")
    except Exception as e:
        logging.error(f"Failed to ensure Kafka topic '{topic_name}': {e}")
        raise RuntimeError(f"Error ensuring Kafka topic: {e}")


consumer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "notification_group",
    "auto.offset.reset": "latest",
    "enable.auto.commit": False,
}

consumer = Consumer(consumer_config)


async def process_message(message):
    try:
        data = json.loads(message.value().decode("utf-8"))
        print("Processed Message Data ====>>>> ",data)
    except ValidationError as e:
        logging.error(f"Message validation failed: {e}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")
    return False

def commit_offsets(message):
    try:
        consumer.commit(message, asynchronous=False)
    except Exception as e:
        logging.error(f"Failed to commit offset: {e}")

async def consume_messages():
    ensure_kafka_topic(TOPIC_NAME)  # Ensure the topic exists
    consumer.subscribe([TOPIC_NAME])
    while True:
        msg = consumer.poll(1.0)
        print("Message ===>>> ", msg)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.info(f"End of partition reached: {msg.partition}")
                continue
            else:
                logging.error(f"Kafka error: {msg.error()}")
                break
        try:
            success = await process_message(msg)
            if success:
                commit_offsets(msg)
            else:
                logging.error("Message processing failed, not committing offset.")
        except Exception as e:
            logging.error(f"Failed to process message: {e}")
            commit_offsets(msg)




if __name__ == "__main__":
    asyncio.run(consume_messages())
