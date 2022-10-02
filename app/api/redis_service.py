import json
import time

from app.extensions import redis_client

CHANNEL = "test"


class RedisService(object):
    @classmethod
    def publish(cls):
        while redis_client.get("is_publish") == 1:
            redis_client.publish(
                channel=CHANNEL,
                message=json.dumps({
                    "tuan": time.time(),
                })
            )
            time.sleep(1)
        redis_client.set("is_publish", 0)

    @classmethod
    def subscribe(cls):
        pub = redis_client.pubsub()
        pub.subscribe(CHANNEL)
        for message in pub.listen():
            if message is not None and isinstance(message, dict) and message.get("data") != 1:
                data = json.loads(message.get('data'))
                # print(data["tuan"])
                print(f"Message: {data}")

    @classmethod
    def stream(cls):
        data = {
            "tuan": time.time(),
        }
        redis_client.xadd('order_completed', data, "*")
        pass
