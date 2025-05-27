import serial
import time
import os
from datetime import datetime

# AT 포트 설정 (보통 /dev/ttyUSB2)
PORT = "/dev/ttyUSB2"
BAUDRATE = 115200

# 로그 디렉토리 생성
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 로그 파일명 (시간 기반)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(log_dir, f"lte_log_{timestamp}.txt")

def send_at_command(ser, command, delay=1.0):
    ser.write((command + '\r\n').encode())
    time.sleep(delay)
    output = ser.read_all().decode(errors="ignore")
    return output

def parse_cesq(response):
    # +CESQ: <rxlev>,<ber>,<rscp>,<ecno>,<rsrq>,<rsrp>
    for line in response.splitlines():
        if "+CESQ:" in line:
            parts = line.split(":")[1].strip().split(",")
            if len(parts) == 6:
                return {
                    "rxlev(RSSI)": parts[0],
                    "ber": parts[1],
                    "rscp": parts[2],
                    "ecno": parts[3],
                    "rsrq": parts[4],
                    "rsrp": parts[5],
                }
    return None

def log_lte_status():
    with serial.Serial(PORT, BAUDRATE, timeout=2) as ser:
        with open(log_path, "a") as f:
            while True:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ser.reset_input_buffer()
                result = send_at_command(ser, "AT+CESQ")
                signal = parse_cesq(result)
                if signal:
                    log_line = f"[{now}] CESQ → " + ", ".join([f"{k}: {v}" for k, v in signal.items()])
                    print(log_line)
                    f.write(log_line + "\n")
                else:
                    print(f"[{now}] CESQ 응답 파싱 실패:\n{result}")
                    f.write(f"[{now}] CESQ 응답 파싱 실패:\n{result}\n")
                time.sleep(10)  # 10초마다 측정

if __name__ == "__main__":
    print(f"LTE 신호 측정 시작 → 로그 파일: {log_path}")
    log_lte_status()
