import requests
import time

SERVER_URL = "http://210.107.220.232:5000"
target_device = "device1"
last_ping_time = None

while True:
    try:
        res = requests.get(f"{SERVER_URL}/listen")
        ping_data = res.json()
    except:
        
        continue

    if target_device not in ping_data:
        
        continue

    ping_time = ping_data[target_device]["time"]

    if last_ping_time is None or ping_time != last_ping_time:
        print(f"[LISTEN] new ping has arrived: {ping_time}")
        res = requests.post(f"{SERVER_URL}/pong", json={
            "to": target_device,
            "ping_time": ping_time
        })
        print("✅ pong is transmitted")
        last_ping_time = ping_time


    