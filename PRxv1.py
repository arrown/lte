import requests
import json
import csv
import os

SERVER_URL = "http://210.107.220.232:5000"
target_device = "device1"

listen_url = f"{SERVER_URL}/listen-sse?device={target_device}"
print(f"📡 Listening for ping from {target_device}...")

log_data = []  # 로그 누적 리스트
LOG_THRESHOLD = 40
LOG_FILENAME = "pong_log.csv"

# CSV 헤더 쓰기 (최초 1회만)
if not os.path.exists(LOG_FILENAME):
    with open(LOG_FILENAME, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ping_time_ms", "rtt_ms"])

with requests.get(listen_url, stream=True) as response:
    for line in response.iter_lines():
        if line:
            decoded = line.decode("utf-8")

            if decoded.startswith("data:"):
                try:
                    json_data = decoded.replace("data: ", "")
                    ping_info = json.loads(json_data)

                    ping_time = ping_info.get("ping_time")
                    if ping_time is None:
                        print("❌ No ping_time received.")
                        continue

                    print(f"✅ Received ping: {float(ping_time):.2f} ms")

                    pong_url = f"{SERVER_URL}/pong"
                    res = requests.post(pong_url, json={
                        "to": target_device,
                        "ping_time": ping_time
                    })

                    pong_result = res.json()
                    rtt = pong_result.get("rtt_ms")
                    if rtt is not None:
                        print(f"📤 Sent pong | RTT: {rtt:.2f} ms")
                        log_data.append((ping_time, rtt))

                        # 40개 모이면 저장
                        if len(log_data) >= LOG_THRESHOLD:
                            with open(LOG_FILENAME, mode="a", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerows(log_data)
                            print(f"📁 Saved {len(log_data)} records to '{LOG_FILENAME}'")
                            log_data.clear()

                    else:
                        print("⚠️ Pong failed | Server says:", pong_result)

                except Exception as e:
                    print(f"❌ Error handling ping/pong: {e}")