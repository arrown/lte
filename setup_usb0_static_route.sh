#!/bin/bash

# 백업 먼저
sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.bak.$(date +%s)

# 설정 추가
echo "" | sudo tee -a /etc/dhcpcd.conf
echo "# ===== LTE usb0 설정 =====" | sudo tee -a /etc/dhcpcd.conf
echo "interface usb0" | sudo tee -a /etc/dhcpcd.conf
echo "static ip_address=192.168.225.30/24" | sudo tee -a /etc/dhcpcd.conf
echo "static routers=192.168.225.1" | sudo tee -a /etc/dhcpcd.conf
echo "static domain_name_servers=8.8.8.8 1.1.1.1" | sudo tee -a /etc/dhcpcd.conf

echo ""
echo "✅ 설정이 /etc/dhcpcd.conf 에 추가되었습니다."
echo "🔁 시스템을 재부팅하여 적용하세요: sudo reboot"
