"""
Configures the Kafka consumer using environment variables.

Reads from a `.env` file to set Kafka consumer parameters.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class KafkaConfig:
    """
    Configuration class for Kafka settings.

    This class loads the Kafka consumer configuration from environment
        variables.
    """
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
    KAFKA_BROKER = os.getenv('KAFKA_BROKER')
    KAFKA_GROUP = os.getenv('KAFKA_GROUP')
    consumer_config = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': KAFKA_GROUP,
        'auto.offset.reset': 'earliest'
    }
