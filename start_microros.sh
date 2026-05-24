#!/bin/bash
# Auto-restart micro-ros-agent
CONTAINER_NAME="microros_agent"

echo "==========================================================="
echo "🤖 Micro-ROS Agent Auto-Restarter"
echo "👉 Bấm Ctrl+C MỘT LẦN để force-restart (Reset) kết nối."
echo "👉 Bấm Ctrl+C HAI LẦN liên tiếp (trong 2s) để THOÁT hoàn toàn."
echo "==========================================================="

LAST_INT=0

# Bắt tín hiệu Ctrl+C
trap '
    NOW=$(date +%s)
    if [ $((NOW - LAST_INT)) -lt 2 ]; then
        echo -e "\n[Thoát] Đang tắt Agent..."
        docker rm -f $CONTAINER_NAME 2>/dev/null
        exit 0
    fi
    LAST_INT=$NOW
    echo -e "\n[Reset] Force-restarting agent..."
    docker rm -f $CONTAINER_NAME 2>/dev/null
' SIGINT

while true; do
    docker rm -f $CONTAINER_NAME 2>/dev/null
    echo "[$(date)] Starting micro-ros-agent (UDP:8888)..."
    echo "-----------------------------------------------------------"

    # Thêm flag -t (pseudo-TTY) để stdout của container là line-buffered (hiển thị log ngay lập tức)
    # Thêm flag --sig-proxy=false để docker không chiếm mất tín hiệu Ctrl+C, giúp trap của bash hoạt động hoàn hảo
    docker run -it --sig-proxy=false --name $CONTAINER_NAME --net=host \
        -e ROS_DOMAIN_ID=10 \
        microros/micro-ros-agent:humble udp4 --port 8888
        
    echo "[$(date)] Agent exited. Tự động khởi động lại sau 1s..."
    sleep 1
done
