import json
import logging
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from sqlalchemy import Enum
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)

# Kafka configuration
producer_config = {"bootstrap.servers": settings.kafka_bootstrap_servers}
producer = Producer(producer_config)
topic = settings.kafka_trigger_topic


def publish_to_kafka(payload):
    """Publishes a message to Kafka with proper logging."""
    ensure_kafka_topic(topic)
    try:
        serialized_payload = json.dumps(payload)
        producer.produce(topic, serialized_payload, callback=acked)
        producer.poll(1)  # Allow the producer to process delivery reports asynchronously
    except Exception as e:
        logging.error(f"Error producing Kafka message: {e}", exc_info=True)


def ensure_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = AdminClient({"bootstrap.servers": settings.kafka_bootstrap_servers})
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


def custom_json_serializer(obj):
    if isinstance(obj, Enum):  # This correctly handles enum instances
        return obj.value  # Convert enum instance to string

    raise TypeError(f"Type {type(obj)} not serializable")


def acked(err, msg):
    """Kafka message acknowledgment callback."""
    if err:
        logging.error(f"Failed to deliver message: {err}")
    else:
        logging.info(f"Message produced : {msg.topic()} [{msg.partition()}]")
