import requests
import time

SERVER_URL = "http://210.107.220.232:5000"
device_name = "device1"

while True:
    # 1️⃣ Send ping
    ping_time = time.time() * 1000  # milliseconds
    try:
        res = requests.post(f"{SERVER_URL}/ping", json={
            "from": device_name,
            "client_time": ping_time
        })
        print(f"[PING] {ping_time:.2f} ms sent")
    except Exception as e:
        print(f"❌ Failed to send ping: {e}")
        time.sleep(2)
        continue

    # 2️⃣ Wait for pong
    for i in range(5):  # Retry up to 5 times (1s interval)
        time.sleep(1)
        try:
            res = requests.get(f"{SERVER_URL}/check", params={"device": device_name})
            pong_data = res.json()
            if "rtt_ms" in pong_data:
                print(f"✅ RTT: {pong_data['rtt_ms']:.2f} ms")
                break
            else:
                print(f"⏳ waiting for pong... ({i+1}/5)")
        except Exception as e:
            print(f"❌ Failed to check pong: {e}")
            break
    else:
        print("❌ timeout")

    print("-" * 30)
    time.sleep(1)