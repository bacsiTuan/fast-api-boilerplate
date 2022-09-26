from app.extensions import redis_client
import time
from dotenv import load_dotenv

load_dotenv(override=False)

key = "order_completed"
group = "inventory-group"

try:
    redis_client.xgroup_create(key, group)
except Exception as e:
    print("group already exists!")

while True:
    try:
        results = redis_client.xreadgroup(
            groupname=group,
            consumername=key,
            streams={key: '>'},
            count=None, noack=True
        )
        if len(results) > 0:
            for result in results:
                print(result)
    except Exception as e:
        print(str(e))
    time.sleep(1)
