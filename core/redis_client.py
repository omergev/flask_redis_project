import redis
import json

# Load configuration
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "../config/appsettings.json")

with open(CONFIG_PATH) as config_file:
    config = json.load(config_file)


# Initiate redis client
def create_redis_client():
    try:
        client = redis.StrictRedis(host=config['Redis']['ConnectionString'])
        # Test the connection
        client.ping()
        return client
    except:
        raise RuntimeError("Redis server is not running. Please start the Redis server and try again.")


ma_redis_client = create_redis_client()
