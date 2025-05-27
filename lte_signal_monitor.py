import serial
import time
import re

# 설정
PORT = "/dev/ttyUSB2"      # AT 명령 가능한 포트
BAUDRATE = 115200
INTERVAL = 10              # 측정 주기 (초)

def send_at_command(ser, command, timeout=2):
    ser.write((command + "\r").encode())
    time.sleep(timeout)
    return ser.read_all().decode(errors='ignore')

def parse_csq(response):
    match = re.search(r'\+CSQ: (\d+),(\d+)', response)
    if match:
        rssi = int(match.group(1))
        ber = match.group(2)
        dbm = -113 + 2 * rssi if rssi < 32 else "Unknown"
        return rssi, ber, dbm
    return None

def parse_servingcell(response):
    match = re.search(r'servingcell","(\w+)",\s*"LTE","\w+",(\d+),\s*(\d+),.*?,.*?,.*?,.*?,.*?,.*?,.*?,(-?\d+),(-?\d+)', response)
    if match:
        conn_state = match.group(1)
        earfcn = match.group(2)
        pci = match.group(3)
        rsrp = match.group(4)
        rsrq = match.group(5)
        return conn_state, earfcn, pci, rsrp, rsrq
    return None

def main():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"[INFO] 포트 {PORT} 연결 성공")

        while True:
            print("\n[INFO] 신호 정보 조회 중...")

            csq_resp = send_at_command(ser, "AT+CSQ")
            csq_result = parse_csq(csq_resp)
            if csq_result:
                rssi, ber, dbm = csq_result
                print(f"  ▶ RSSI: {rssi} → 약 {dbm} dBm, BER: {ber}")
            else:
                print("  ▶ CSQ 정보 파싱 실패")

            qeng_resp = send_at_command(ser, 'AT+QENG="servingcell"')
            qeng_result = parse_servingcell(qeng_resp)
            if qeng_result:
                conn, earfcn, pci, rsrp, rsrq = qeng_result
                print(f"  ▶ 연결 상태: {conn}, EARFCN: {earfcn}, PCI: {pci}")
                print(f"  ▶ RSRP: {rsrp} dBm, RSRQ: {rsrq} dB")
            else:
                print("  ▶ QENG 정보 파싱 실패")

            time.sleep(INTERVAL)

    except serial.SerialException as e:
        print(f"[ERROR] 포트 연결 실패: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] 종료됨.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()