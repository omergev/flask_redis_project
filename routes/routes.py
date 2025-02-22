import base64
from datetime import datetime
import uuid

from flask import Blueprint, request, jsonify, Response
from flask_redis_project.core.redis_client import ma_redis_client

echo_at_time_bp = Blueprint('echo_at_time', __name__)
health_check_bp = Blueprint('health_check', __name__)

REDIS_KEY = "scheduled_messages"

LOCK_TIMEOUT = 5
NUM_MESSAGES = 100

@echo_at_time_bp.route('', methods=['POST'])
def echo_at_time():
    # Logic to save to redis will be added here
    try:
        data = request.get_json()
        timestamp = int(data['time'])  # Time in milliseconds
        unique_id = str(uuid.uuid4())
        message = data['message']
        unique_message = f"{unique_id} : {message}"

        now = int(datetime.now().timestamp() * 1000)
        if timestamp < now:
            return jsonify({"status": "error", "error": "Timestamp should be in the future"}), 400

        # Save message in a Redis sorted set with timestamp as score
        ma_redis_client.zadd(REDIS_KEY, {unique_message: timestamp})

        return jsonify({"status": "success", "message": "Message scheduled"}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@health_check_bp.route('', methods=['GET'])
def health_check():
    base64_image = 'IC4uLiAgICAuLi4gICAuLi4uLi4gIC4uLi4uLiAgLi4uICAuLi4gICAjIyMjICAjIyMjIyggIyMjIyMjIyAlIyMgIyMsICAlIyMgIyMvLy4KIC4uLi4gICAuLi4gIC4uLiAgLi4gLi4uICAuLiAgLi4uICAuLi4gICAjIyMjICAoIyMgICAgICAjIyMgICAqJSUgJSMjICAjIyAgIyMgICAKIC4uLi4uIC4uLi4uIC4uLiAgLi4uLi4uICAuLi4gLi4uLiAuLi4gICUjJSMjKCAvIyMgICAgICAjIyMgICAsIyMgLiMjIC4jIyAgIyMgICAKIC4uLi4uIC4uLi4uIC4uLiAgLi4uLi4uICAuLi4gLi4uLi4uLi4gICMjIC4jIyAqIyMgICAgICAjIyMgICAqIyMgICMjICUjIyAgIyMgICAKIC4uLi4uLi4uLi4uIC4uLiAgLi4uLi4uICAuLi4gLi4uLi4uLi4gICMjIyMjIyAuIyMgICAgICAjIyMgICAoIyMgICMjLyMjLiAgIyMjIyAKIC4uIC4uLi4uIC4uIC4uLiAgLi4uLi4uICAuLi4gLi4gLi4uLi4gKiMjICAjIyAgIyMsICAgICAjIyMgICAlIyMgICgjIyMjICAgIyMgICAKIC4uIC4uLi4gIC4uLiAuLiAgLi4gIC4uICAuLiAuLi4gIC4uLi4gJSMjICAjIy8gIyMjICAgICAjIyMgICAlIyMgICAjIyMjICAgIyMgICAKLi4uICAuLi4gIC4uLiAuLi4uLi4gIC4uLi4uLiAuLi4gIC4uLi4gIyMsICAjIyMgIyMjIyMgICAjIyMgICAoIyMgICAjIyMvICAgIyMjIyM='
    image = base64.b64decode(base64_image).decode('utf-8')
    print(ma_redis_client.set('key', 'value'))
    print(ma_redis_client.get('key'))
    return Response(image, mimetype='text/plain')


def fetch_and_print_messages():
    """Fetch and print messages from Redis at the right time."""
    try:
        now = int(datetime.now().timestamp() * 1000)

        # Fetch messages whose time has come (score <= now)
        messages = ma_redis_client.zrangebyscore(REDIS_KEY, 0, now, start=0, num=NUM_MESSAGES)

        for message in messages:
            message = message.decode('utf-8')
            message_data = message.split(":", 1)
            unique_id = message_data[0]
            message_content = message_data[1]

            lock_key = f"lock:{unique_id}"
            lock = ma_redis_client.set(lock_key, "1", nx=True, ex=LOCK_TIMEOUT)

            if lock:
                try:
                    print(f"{message_content}")
                    ma_redis_client.zrem(REDIS_KEY, message)
                except Exception as e:
                    print(f"Error printing message {message}: {e}")
                finally:
                    ma_redis_client.delete(lock_key)

    except Exception as e:
        print(f"Error in fetch_and_print_messages: {e}")
