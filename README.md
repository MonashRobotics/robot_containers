
## ROS2 base image

docker build . -f Dockerfile.ros2 -t ros2-base

https://github.com/osrf/rocker/tree/main/src/rocker/templates

https://github.com/dusty-nv/jetson-containers

## How to create a .repos file for use by vcstool

```
git clone https://repo-a.git
git clone https://repo-b.git
vcs export > sourcecode.repos
```