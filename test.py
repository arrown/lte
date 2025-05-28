import requests

SERVER_URL = "http://210.107.220.232:5000"

try:
    res = requests.post(f"{SERVER_URL}/ping", json={"from": "test", "client_time": 1234}, timeout=3)
    print(f"✅ HTTP 연결 성공: {res.status_code} | 응답: {res.text}")
except requests.exceptions.RequestException as e:
    print(f"❌ HTTP 요청 실패: {e}")
