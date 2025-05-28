import requests
import time

SERVER_URL = "http://218.146.74.22:5000"
device_name = "device1"

while True:
    # 1️⃣ ping 전송
    ping_time = time.time()
    res = requests.post(f"{SERVER_URL}/ping", json={
        "from": device_name,
        "client_time": ping_time
    })
    print(f"[PING] 전송 시간: {ping_time}")

    # 2️⃣ pong 응답 대기
    for _ in range(10):  # 최대 10초 대기
        time.sleep(1)
        res = requests.get(f"{SERVER_URL}/check", params={"device": device_name})
        result = res.json()
        if "rtt" in result:
            print(f"✅ pong 수신 | RTT: {round(result['rtt'], 4)}초")
            break
        else:
            print("⏳ pong 대기 중...")
    else:
        print("❌ pong 수신 실패 (timeout)")

    print("-" * 30)
    time.sleep(2)  # 다음 ping까지 2초 대기