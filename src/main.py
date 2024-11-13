"""
Entrypoint that starts the consumers
"""
from src.services.kafka_manager import start_consumer

if __name__ == "__main__":
    start_consumer()
