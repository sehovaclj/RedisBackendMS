"""
Entrypoint that starts the consumers
"""
from src.utils.kafka_utils import start_consumer

if __name__ == "__main__":
    start_consumer()
