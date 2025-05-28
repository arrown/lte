import requests
import time

SERVER_URL = "http://210.107.220.232:5000"
device_name = "device1"

while True:
    # 1️⃣ transmit ping
    ping_time = time.time()
    res = requests.post(f"{SERVER_URL}/ping", json={
        "from": device_name,
        "client_time": ping_time
    })
    print(f"[PING] transmition time : {ping_time}")

    # 2️⃣ waiting for pong
    for _ in range(3):  # max 3 seconds wait
        time.sleep(1)
        res = requests.get(f"{SERVER_URL}/check", params={"device": device_name})
        result = res.json()
        if "rtt" in result:
            print(f"✅ pong has received | RTT: {round(result['rtt'], 4)}sec")
            break
        else:
            print("⏳ waiting for pong")
    else:
        print("❌ no response within 3 seconds (timeout)")

    print("-" * 30)
    time.sleep(0.5)  # transmit ping every 0.5 seconds