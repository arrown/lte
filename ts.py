import requests, json, csv, os, threading
from datetime import datetime

SERVER_URL = "http://222.112.76.252:5000"
target_device = "device1"
listen_url = f"{SERVER_URL}/listen-sse?device={target_device}"
pong_url = f"{SERVER_URL}/pong"
LOG_FILENAME = "pong_log.csv"
LOG_THRESHOLD = 40

session = requests.Session()
log_data = []

def save_log():
    global log_data
    if log_data:
        with open(LOG_FILENAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(log_data)
        print(f"📁 Saved {len(log_data)} records")
        log_data = []

print(f"📡 Listening for ping from {target_device}...")

# 헤더 저장 (최초 1회)
if not os.path.exists(LOG_FILENAME):
    with open(LOG_FILENAME, "w", newline="") as f:
        csv.writer(f).writerow(["ping_time_ms", "rtt_ms"])

with session.get(listen_url, stream=True) as response:
    for line in response.iter_lines():
        if line and line.startswith(b"data:"):
            try:
                ping_info = json.loads(line.decode()[6:])
                ping_time = ping_info.get("ping_time")
                if ping_time is None:
                    continue

                print(f"✅ Ping: {float(ping_time):.2f} ms")

                res = session.post(pong_url, json={"to": target_device, "ping_time": ping_time})
                pong_result = res.json()
                rtt = pong_result.get("rtt_ms")

                if rtt is not None:
                    print(f"📤 Pong | RTT: {rtt:.2f} ms")
                    log_data.append((ping_time, rtt))
                    if len(log_data) >= LOG_THRESHOLD:
                        threading.Thread(target=save_log).start()
                else:
                    print("⚠️ Pong failed:", pong_result)
            except Exception as e:
                print("❌ Error:", e)