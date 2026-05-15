#!/bin/bash
# Auto-restart micro-ros-agent khi crash
CONTAINER_NAME="microros_agent"

while true; do
    # Dọn dẹp container cũ
    docker rm -f $CONTAINER_NAME 2>/dev/null
    
    echo "[$(date)] Starting micro-ros-agent (Waiting for Robot connection...)"
    # Thêm -it và --user để giống lệnh gốc của bạn
    docker run -it --name $CONTAINER_NAME --net=host \
        --user=$(id -u):$(id -g) \
        microros/micro-ros-agent:humble udp4 --port 8888
    
    EXIT_CODE=$?
    # Nếu thoát bằng Ctrl+C (code 130), thì dừng hẳn vòng lặp
    if [ $EXIT_CODE -eq 130 ]; then
        echo "Stopped by user."
        break
    fi
    
    echo "[$(date)] Agent exited with code $EXIT_CODE. Restarting in 2s..."
    sleep 2
done
