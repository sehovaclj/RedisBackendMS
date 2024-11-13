"""
Utility module for connecting to a Redis database.

Functions:
    connect_to_redis: Connects to Redis and returns a Redis client or None
        if the connection fails.
"""

# initialize the connection to redis
redis_client = connect_to_redis()


def store_and_publish_redis(message):
    """
    Processes each message by storing it in Redis and publishing to
        Redis subscriber.

    Args:
        message (dict): The Kafka consumer message to be processed.
    """
    # get our main key_id
    battery_id = message.pop('battery_id', "-1")
    # build our redis key
    redis_key = f"battery:{battery_id}"

    # Use a pipeline for bulk operations
    with redis_client.pipeline() as pipe:
        for key, value in message.items():
            # Set each key-value in Redis
            pipe.set(f"{redis_key}:{key}", value)
            # Publish each key-value pair to a specific channel
            pipe.publish(f"{redis_key}:{key}", "updates")

        # Execute all commands in the pipeline at once
        pipe.execute()
