#!/usr/bin/env bash
exec ros2 run web_video_server web_video_server \
  --ros-args \
  -p port:=8080 \
  -p address:=127.0.0.1 \
  -p default_qos_profile:=sensor_data