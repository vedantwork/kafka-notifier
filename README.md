# 📌 Kafka Notification System

This project implements a Kafka-based notification system using Python with `confluent-kafka`. It includes a Kafka producer to publish messages and a Kafka consumer to process them.

---

## 📜 Table of Contents
1. 📝 [Overview](#-overview)
2. 📂 [Project Structure](#-project-structure)
3. 🚀 [Kafka Producer (Publishing Messages)](#-kafka-producer-publishing-messages)
4. 🎯 [Kafka Consumer (Processing Messages)](#-kafka-consumer-processing-messages)
5. 🛠 [Kafka Topic Management](#-kafka-topic-management)
6. ▶️ [How to Run](#-how-to-run)
7. ⚠️ [Error Handling](#-error-handling)
8. 🔗 [Download & Setup Links](#-download--setup-links)

---

## 📝 Overview
This system consists of two main components:
1. **Kafka Producer** - Publishes messages to a Kafka topic.
2. **Kafka Consumer** - Consumes messages from the Kafka topic and processes them.

Each component ensures that Kafka topics exist before producing or consuming messages. The messages are serialized as JSON before publishing.

![Kafka Workflow](https://upload.wikimedia.org/wikipedia/commons/0/05/Apache_kafka.svg)

---

## 📂 Project Structure
```
project/
│── publish_to_kafka.py  # Defines code to publish the payload
│── kafka_service.py     # Defines the Kafka Producer
│── consumer.py          # Defines the Kafka Consumer
│── .env                 # Environment variables
│── config.py            # Configuration settings
│── README.md            # Documentation
```

---

## 🚀 Kafka Producer (Publishing Messages)
The `kafka_service.py` file defines a producer that publishes messages to a Kafka topic.

### 🔹 Key Functions:
1. **`publish_to_kafka(payload)`**: 
   - Ensures the topic exists using `ensure_kafka_topic()`.
   - Serializes the payload as JSON.
   - Publishes the message to Kafka.
   - Calls `flush()` to ensure the message is sent immediately.

2. **`ensure_kafka_topic(topic_name)`**: 
   - Checks if the Kafka topic exists.
   - If not, creates the topic with default partitions and replication factor.

3. **`acked(err, msg)`**: 
   - Callback function to check if a message was successfully published.

#### 📌 Sample Code for Publishing Messages:
```python
try:
    publish_to_kafka(payload)
except Exception as e:
    logger.error("Kafka error while publishing payload: ", e)
```

---

## 🎯 Kafka Consumer (Processing Messages)
The `consumer.py` file defines a consumer that reads messages from the Kafka topic.

### 🔹 Key Functions:
1. **`consume_messages()`**: 
   - Ensures the topic exists before consuming.
   - Subscribes to the topic and continuously polls for new messages.
   - Calls `process_message()` for each received message.
   - If successful, commits the message offset.

2. **`process_message(message)`**: 
   - Decodes and processes the message.
   - Logs any errors that occur during processing.

3. **`commit_offsets(message)`**: 
   - Commits the message offset after successful processing.

#### 📌 Sample Code for Consuming Messages:
```python
if __name__ == "__main__":
    asyncio.run(consume_messages())
```

---

## 🛠 Kafka Topic Management
Both producer and consumer include the **`ensure_kafka_topic()`** function to:
- ✅ Verify if the topic exists.
- ➕ If not, create it dynamically.

---

## ▶️ How to Run
### 🔧 1. Set Up Kafka
Ensure that Kafka is installed and running.

```sh
# Start Zookeeper in a new terminal
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker in another terminal
bin/kafka-server-start.sh config/server.properties
```

### 🔧 2. Configure Environment Variables
Create a `.env` file and set the following variables:
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TOPIC_NAME=notifications
```

### 🔧 3. Manage Kafka Topics
```sh
# Delete an existing topic
bin/kafka-topics.sh --delete --topic notifications --bootstrap-server localhost:9092

# Create a new topic
bin/kafka-topics.sh --create --topic notifications --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 🔧 4. Run the Kafka Producer
```sh
python kafka_service.py
```

### 🔧 5. Run the Kafka Consumer
```sh
python consumer.py
```

### 🔧 6. Consume Messages from Kafka Console
```sh
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic notifications --from-beginning
```

---

## ⚠️ Error Handling
1. **Producer Errors**:
   - ❌ If message publishing fails, an error is logged.
   - 🔄 The producer flushes messages to ensure they are sent.

2. **Consumer Errors**:
   - ❌ If message processing fails, it is logged and offset is not committed.
   - ⚙️ Kafka errors are logged and handled appropriately.

---

## 🔗 Download & Setup Links
1. **Download Apache Kafka**: [Kafka Official Download](https://kafka.apache.org/downloads)
2. **Install Java (Required for Kafka)**: [Download Java](https://www.oracle.com/java/technologies/javase-jdk17-downloads.html)
3. **Install Python Dependencies**:
   ```sh
   pip install confluent-kafka python-dotenv
   ```
4. **Kafka Documentation**: [Kafka Official Docs](https://kafka.apache.org/documentation/)

---

## 🎯 Conclusion
This system provides a robust way to publish and consume messages using Kafka. It ensures that topics exist before publishing and consuming messages and includes error handling mechanisms to handle failures gracefully.

