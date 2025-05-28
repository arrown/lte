#!/bin/bash

echo "🚀 GPS 초기화 시작: $(date)" >> /var/log/gps_start.log

# 최대 30초 동안 ttyUSB2 등장 기다림
for i in {1..30}; do
    if [ -e /dev/ttyUSB2 ]; then
        echo "✅ /dev/ttyUSB2 발견됨" >> /var/log/gps_start.log
        break
    fi
    echo "⏳ /dev/ttyUSB2 대기 중... ($i초)" >> /var/log/gps_start.log
    sleep 1
done

# 장치 없으면 종료
if [ ! -e /dev/ttyUSB2 ]; then
    echo "❌ /dev/ttyUSB2 미발견. GPS 초기화 실패." >> /var/log/gps_start.log
    exit 1
fi

# AT 명령 전송
echo -e "AT+CGPS=1,1\r" > /dev/ttyUSB2
echo "📡 AT 명령 전송 완료 (AT+CGPS=1,1)" >> /var/log/gps_start.log

exit 0
