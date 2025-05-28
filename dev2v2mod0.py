import requests
import time

SERVER_URL = "http://218.146.74.22:5000"
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
        print(f"[LISTEN] 새 ping 감지: {ping_time}")
        res = requests.post(f"{SERVER_URL}/pong", json={
            "to": target_device,
            "ping_time": ping_time
        })
        print("✅ pong 전송 완료")
        last_ping_time = ping_time
    else:
        print("🔁 동일 ping. 대기 중...")

    