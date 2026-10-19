FROM osrf/ros:kilted-desktop

SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    vim \
    ros-kilted-rosidl-default-generators \
    ros-kilted-rosidl-default-runtime \
    ros-kilted-ros-environment \
    ros-kilted-ament-cmake \
    ros-kilted-builtin-interfaces \
    ros-kilted-std-msgs \
    ros-kilted-vision-msgs \
    ros-kilted-geometry-msgs \
    ros-kilted-diagnostic-msgs \
    ros-kilted-web-video-server \
    ros-kilted-rosbridge-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/carla_ws/src
RUN git clone https://github.com/carla-simulator/ros-carla-msgs.git

WORKDIR /opt/carla_ws

RUN source /opt/ros/kilted/setup.bash && \
    colcon build --packages-select carla_msgs

RUN printf '%s\n' \
    'source /opt/ros/kilted/setup.bash' \
    'source /opt/carla_ws/install/setup.bash' \
    'if [ -f /workspace/ros2_ws/install/setup.bash ]; then' \
    '    source /workspace/ros2_ws/install/setup.bash' \
    'fi' \
    >> /root/.bashrc

WORKDIR /workspace