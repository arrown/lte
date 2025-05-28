import requests
import time

SERVER_URL = "http://210.107.220.232:5000"
device_name = "device1"

while True:
    # 1️⃣ Ping 전송
    ping_time = round(time.time() * 1000, 3)  # ms 단위 (float)
    try:
        res = requests.post(f"{SERVER_URL}/ping", json={
            "from": device_name,
            "client_time": ping_time
        })
        if res.status_code == 200:
            print(f"[PING] {ping_time:.3f} ms 전송 완료")
        else:
            print(f"❌ ping 전송 실패 | 상태코드: {res.status_code}")
            time.sleep(1)
            continue
    except Exception as e:
        print(f"❌ ping 전송 오류: {e}")
        time.sleep(1)
        continue

    # 2️⃣ pong 응답 대기
    success = False
    for i in range(3):  # 3초간 대기
        time.sleep(1)
        try:
            res = requests.get(f"{SERVER_URL}/check", params={"device": device_name})
            if res.status_code != 200:
                print(f"⚠️ 서버 응답 이상: {res.status_code}")
                continue

            pong_data = res.json()
            rtt = pong_data.get("rtt_ms")

            if rtt is not None:
                print(f"✅ pong 수신 | RTT: {rtt:.3f} ms")
                success = True
                break
            else:
                print(f"⏳ pong 대기 중... ({i + 1}/3)")

        except Exception as e:
            print(f"❌ pong 수신 오류: {e}")
            break

    if not success:
        print("❌ pong 수신 실패 (timeout)")

    print("-" * 40)
    time.sleep(1)  # 다음 ping 전송까지 대기