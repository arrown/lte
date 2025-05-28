import requests
import json
import csv
import os

SERVER_URL = "http://210.107.220.232:5000"
target_device = "device1"

listen_url = f"{SERVER_URL}/listen-sse?device={target_device}"
print(f"📡 {target_device}의 ping 수신 대기 중...")

log_data = []
LOG_THRESHOLD = 40
LOG_FILENAME = "pong_log.csv"

# CSV 파일이 없다면 헤더 작성
if not os.path.exists(LOG_FILENAME):
    with open(LOG_FILENAME, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ping_time_ms", "rtt_ms"])

# SSE 연결
with requests.get(listen_url, stream=True) as response:
    for line in response.iter_lines():
        if line:
            decoded = line.decode("utf-8")

            if decoded.startswith("data:"):
                try:
                    # ping 데이터 파싱
                    json_data = decoded.replace("data: ", "")
                    ping_info = json.loads(json_data)

                    ping_time = ping_info.get("ping_time")
                    if ping_time is None:
                        print("❌ ping_time 없음")
                        continue

                    print(f"✅ ping 수신: {float(ping_time):.2f} ms")

                    # pong 전송
                    pong_url = f"{SERVER_URL}/pong"
                    res = requests.post(pong_url, json={
                        "to": target_device,
                        "ping_time": ping_time
                    })

                    pong_result = res.json()
                    rtt = pong_result.get("rtt_ms")
                    if rtt is not None:
                        print(f"📤 pong 전송 완료 | RTT: {rtt:.2f} ms")
                        log_data.append((ping_time, rtt))

                        # 40개 누적되면 CSV로 저장
                        if len(log_data) >= LOG_THRESHOLD:
                            with open(LOG_FILENAME, mode="a", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerows(log_data)
                            print(f"📁 {len(log_data)}개 기록 저장됨 → '{LOG_FILENAME}'")
                            log_data.clear()

                    else:
                        print("⚠️ pong 전송 실패 | 서버 응답:", pong_result)

                except Exception as e:
                    print(f"❌ 처리 중 오류 발생: {e}")