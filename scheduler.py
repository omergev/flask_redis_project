import time
from threading import Thread
from routes import fetch_and_print_messages
from redis_client import ma_redis_client

def start_scheduler():
    def scheduler():
        while True:
            time.sleep(1)
            fetch_and_print_messages()

    thread = Thread(target=scheduler, daemon=True)
    thread.start()
