#!/bin/bash

echo "🔧 GPS 자동화 설정 시작..."

### 1. /etc/default/gpsd 설정
echo "🛠 /etc/default/gpsd 설정"
sudo bash -c 'cat <<EOF > /etc/default/gpsd
START_DAEMON="true"
GPSD_OPTIONS="-n"
DEVICES="/dev/ttyUSB1"
USBAUTO="false"
EOF'

### 2. chrony.conf 설정 (GPS 동기화용)
echo "🛠 /etc/chrony/chrony.conf 수정"
sudo sed -i '/refclock SHM/d' /etc/chrony/chrony.conf
echo "refclock SHM 0 offset 0.5 delay 0.2 refid GPS" | sudo tee -a /etc/chrony/chrony.conf

### 3. GPS 전원 ON 스크립트 생성
echo "⚡ GPS 전원 켜는 스크립트 생성"
cat <<EOF | sudo tee /usr/local/bin/start_gps_at.sh
#!/bin/bash
echo -e "AT+CGPS=1,1\r" > /dev/ttyUSB2
EOF
sudo chmod +x /usr/local/bin/start_gps_at.sh

### 4. rc.local 자동 실행 설정
echo "🛠 /etc/rc.local 수정"
if ! grep -q "start_gps_at.sh" /etc/rc.local; then
  sudo sed -i '/^exit 0/i /usr/local/bin/start_gps_at.sh' /etc/rc.local
fi
sudo chmod +x /etc/rc.local

### 5. 서비스 재시작
echo "🔁 서비스 재시작 중..."
sudo systemctl enable gpsd
sudo systemctl restart gpsd
sudo systemctl restart chrony

echo "✅ 설정 완료! 재부팅 후 GPS 자동 활성화 및 시간 동기화가 적용됩니다."
echo "🔁 지금 바로 재부팅하려면: sudo reboot"
