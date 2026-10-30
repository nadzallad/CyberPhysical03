FROM ros:humble-ros-base-jammy

ARG USERNAME=dev
ARG UID=1000
ARG GID=1000

SHELL ["/bin/bash", "-c"]

# 1. Dependensi sistem
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    ros-humble-demo-nodes-cpp \
    ros-humble-demo-nodes-py \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-turtlebot3 \
    ros-humble-turtlebot3-msgs \
    ros-humble-turtlebot3-simulations \
    ros-humble-xacro \
    ros-humble-tf2-tools \
    ros-humble-rqt-tf-tree \
    ros-humble-teleop-twist-keyboard \
    liburdfdom-tools \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# 2. User non-root
RUN groupadd -g ${GID} ${USERNAME} 2>/dev/null || true && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USERNAME}


RUN usermod -aG video ${USERNAME} && \
    echo "source /usr/share/gazebo/setup.sh" >> /home/${USERNAME}/.bashrc && \
    echo 'export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models' \
      >> /home/${USERNAME}/.bashrc


COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER ${USERNAME}
WORKDIR /ws

# 3. Kode sumber
COPY --chown=${UID}:${GID} src/ /ws/src/

RUN source /opt/ros/humble/setup.bash && colcon build

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
