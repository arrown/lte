import serial
import os
import time
from datetime import datetime

# Configuration
PORT = "/dev/ttyUSB2"
BAUDRATE = 115200
NUM_MEASUREMENTS = 20  # Total measurements
DELAY = 0.3  # Delay between commands

# Setup log file
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(log_dir, f"lte_signal_log_{timestamp}.txt")

def send_at_command(ser, command):
    ser.reset_input_buffer()
    ser.write((command + '\r\n').encode())
    ser.flush()
    time.sleep(DELAY)
    return ser.read_all().decode(errors="ignore")

def parse_csq(response):
    for line in response.splitlines():
        if "+CSQ:" in line:
            try:
                parts = line.split(":")[1].strip().split(",")
                rssi = int(parts[0])
                ber = parts[1]
                dbm = -113 + 2 * rssi if rssi < 32 else "Unknown"
                return rssi, dbm, ber
            except:
                return None
    return None

def parse_cesq(response):
    for line in response.splitlines():
        if "+CESQ:" in line:
            parts = line.split(":")[1].strip().split(",")
            if len(parts) == 6:
                rsrq = parts[4].strip()
                rsrp = parts[5].strip()
                return rsrq, rsrp
    return None

def measure_lte_signal():
    with serial.Serial(PORT, BAUDRATE, timeout=2) as ser:
        with open(log_path, "a") as f:
            print(f"[INFO] Logging to → {log_path}")
            for i in range(NUM_MEASUREMENTS):
                line = f"[#{i+1}] "

                csq_raw = send_at_command(ser, "AT+CSQ")
                csq = parse_csq(csq_raw)
                if csq:
                    rssi, dbm, ber = csq
                    line += f"RSSI: {rssi} ({dbm} dBm), BER: {ber}; "
                else:
                    line += "Failed to parse CSQ; "

                cesq_raw = send_at_command(ser, "AT+CESQ")
                cesq = parse_cesq(cesq_raw)
                if cesq:
                    rsrq, rsrp = cesq
                    line += f"RSRQ: {rsrq}, RSRP: {rsrp}"
                else:
                    line += "Failed to parse CESQ"

                print(line)
                f.write(line + "\n")

if __name__ == "__main__":
    try:
        measure_lte_signal()
        print("[INFO] Finished 20 measurements.")
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user. Exiting...")
