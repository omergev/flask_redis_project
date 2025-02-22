import time
from threading import Thread
from flask_redis_project.routes.routes import fetch_and_print_messages

def start_scheduler():
    def scheduler():
        while True:
            time.sleep(1)
            fetch_and_print_messages()

    thread = Thread(target=scheduler, daemon=True)
    thread.start()
