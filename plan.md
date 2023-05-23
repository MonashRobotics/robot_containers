
# Base image variants:
- ros2
- ros1
- exact ROS version can be an ARG?
- with and without pytorch
- with and without nvidia
- ARM architecture support? (probs just stick with x86)

# Robots
- Fetch
- Baxter
- Jackal
- Pepper
- Panda
- UR5
- Ridgeback
- ABB Yumi

# Drivers
- Velodyne Lidar
- Realsense Cameras
- Zed X Cameras
- Vicon System


# Tasks
- Audit all the robots, create docker files for them
- Include standard drivers
- Upload to the docker image registry

### Notes on GUI/GPU support

https://github.com/osrf/rocker/tree/main/src/rocker/templates

https://github.com/dusty-nv/jetson-containers

### How to create a .repos file for use by vcstool

```
git clone https://repo-a.git
git clone https://repo-b.git
vcs export > sourcecode.repos
```