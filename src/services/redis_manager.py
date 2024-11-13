"""
Module for managing data in a Redis database, as well as storing and
    publishing.

Classes:
    RedisManager: A class to interact with Redis for storing battery data,
    managing battery IDs, and publishing updates.

"""
from typing import List, Dict

from src.db.connection import connect_to_redis


class RedisManager:
    """
    A class to manage Redis interactions for storing and publishing
        battery data.

    Attributes:
        redis_client (redis.Redis): The Redis client connection.
        battery_ids_key (str): Redis key where the list of battery IDs
            is stored.
        battery_ids (List[int]): A local cache of battery IDs for quick
        access.
    """

    def __init__(self):
        """
        Initializes the RedisManager by connecting to Redis, defining
        the battery IDs key, and retrieving the list of existing battery IDs.
        """
        # connect to redis
        self.redis_client = connect_to_redis()
        # Define the key for battery IDs
        self.battery_ids_key = "info:batteries:ids"
        # Initialize the local list of battery IDs
        self.battery_ids = self.get_or_initialize_battery_ids()

    def get_or_initialize_battery_ids(self) -> List[int]:
        """
        Fetch existing battery IDs from Redis or initialize
            if not present.
        """
        battery_ids = self.redis_client.lrange(
            self.battery_ids_key, 0, -1)
        if not battery_ids:  # If list is empty or doesn't exist
            return []
        return [int(bid) for bid in battery_ids]

    def store_and_publish_redis(self, message: Dict[str, int]) -> None:
        """
        Processes each message by storing it in Redis and publishing to
            Redis subscriber.

        Args:
            message (dict): The Kafka consumer message to be processed.
        """
        # get our main key_id
        battery_id = message.pop('battery_id', -1)
        # build our redis key
        redis_key = f"battery:{battery_id}:data"

        # Check if battery_id is in our list, and if not,
        # add it to Redis and local list
        if battery_id not in self.battery_ids:
            self.redis_client.rpush(self.battery_ids_key,
                                    battery_id)  # Append to Redis list
            self.battery_ids.append(battery_id)  # Update local list

        # store message
        self.redis_client.hset(redis_key, mapping=message)
        # publish that new data has been set
        self.redis_client.publish(redis_key, "updates")
