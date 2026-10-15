#!/bin/sh
set -e

. /opt/ros/kilted/setup.sh

echo "Starting rosbridge: $(date)" >> /tmp/post_start.log

nohup setsid -f sh -c \
    'exec ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=9080' \
    > /tmp/rosbridge.log 2>&1 < /dev/null