#!/bin/bash

TARGET="8.8.8.8"                # 대상 IP 또는 도메인
LOG_FILE="nping_log.csv"        # 저장할 로그 파일명
INTERVAL=1                      # 반복 간격 (초)
COUNT=1                         # 반복당 전송 횟수

# CSV 헤더가 없으면 추가
if [ ! -f "$LOG_FILE" ]; then
    echo "timestamp,ip,rtt_ms" >> "$LOG_FILE"
fi

while true
do
    # 현재 시간 기록 (UTC ISO 8601 형식)
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S")

    # nping 실행 (ICMP, 1회)
    RESULT=$(sudo nping --icmp -c $COUNT $TARGET | grep "RTT:")

    # RTT 추출
    RTT=$(echo "$RESULT" | grep -oP 'RTT: \K[0-9.]+' || echo "N/A")

    # 로그 출력 및 저장
    echo "$TIMESTAMP,$TARGET,$RTT" >> "$LOG_FILE"
    echo "[$TIMESTAMP] $TARGET → RTT: $RTT ms"

    # 대기 후 반복
    sleep $INTERVAL
done
