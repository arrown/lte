#!/bin/bash

echo "🔧 [1/5] 필요한 패키지 설치 중..."
sudo apt update
sudo apt install -y usb-modeswitch minicom

echo "🔧 [2/5] 모듈을 ECM 모드로 설정 중..."
sudo minicom -D /dev/ttyUSB2 -b 115200 -C ecm_log.txt -S - <<EOF
AT+CNMP=38
AT+CMNB=3
AT+CGDCONT=1,"IP","internet.ktfwing.com"
AT+CGATT=1
AT$QCRMCALL=1,1
EOF

echo "⏳ 모듈 초기화 및 연결 대기 중 (10초)..."
sleep 10

echo "🔧 [3/5] usb0 인터페이스 존재 확인 중..."
if ip link show usb0 > /dev/null 2>&1; then
    echo "✅ usb0 인터페이스 확인됨"
else
    echo "❌ usb0 인터페이스가 없습니다. 모듈 상태 확인 필요."
    exit 1
fi

echo "🔧 [4/5] 기본 라우팅을 usb0으로 설정 중..."
sudo ip route del default 2>/dev/null
sudo ip route add default dev usb0

echo "🔧 [5/5] DNS 설정(Google DNS 사용)..."
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null

echo "✅ 설정 완료! 인터넷 연결 상태 확인:"
ping -I usb0 -c 4 8.8.8.8
