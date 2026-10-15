#!/usr/bin/env bash

exec docker run --rm -it --init \
    --runtime=nvidia \
    --net=host \
    --env=NVIDIA_VISIBLE_DEVICES=all \
    --env=NVIDIA_DRIVER_CAPABILITIES=all \
    --env=ROS_DOMAIN_ID="0" \
    --env=ROS_LOCALHOST_ONLY="0" \
    --env=RMW_IMPLEMENTATION="rmw_fastrtps_cpp" \
    --name=carla \
    carlasim/carla:0.9.16 bash CarlaUE4.sh -RenderOffScreen -nosound --ros2