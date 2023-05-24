
# Robot Containers
This repository contains Dockerfiles for building containers for various robots.
It also includes a python script for building and running the containers with support for graphical applications, GPU passthrough, realtime scheduling, host networking and full device access.

## Installation

- Install Docker using `sudo apt install docker.io`. Other installation methods may not play well with the nvidia-docker2 runtime.
- Follow "Manage Docker as a non-root user" at https://docs.docker.com/engine/install/linux-postinstall/
- In VSCode install the "Dev Container" extension
- Install nvidia-docker2 by following https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit

## Usage: Creating a new project

Create a folder for your project.
```bash
mkdir my_project
cd my_project
```

Download the `run.py` python script from this repo.

```bash
wget https://raw.githubusercontent.com/MonashRobotics/robot_containers/main/run.py
chmod +x ./run.py
```

Create a file named `Dockerfile` based on one of the existing container images.

```bash
echo "FROM ghcr.io/monashrobotics/ur5-noetic:main" > Dockerfile
```

Use the `run.py` script to build and enter your container:

```bash
./run.py --name my_project
```

So that you don't need to type out your project name every time, you can change the default values in `run.py`:

```Dockerfile
6   # Default values when no arguments are provided.
7   PROJECT_NAME="my_project"
```

Run `./run.py --help` for supported robot and rosdistro combinations.

## Available Containers

| Robot / ROS Distro (Ubuntu OS) | ROS 1 Melodic (18.04) | ROS 1 Noetic (20.04) | ROS 2 Foxy (20.04) | ROS 2 Humble (22.04)
| --- | :---: | :---: | :---: | :---: |
| ABB YuMi | ✅ | ✅ | ❌ | ❌ |
| Baxter | ❌ | ✅ | ❌ | ❌ |
| Fetch | ❌ | ✅ | ❌ | ❌ |
| Jackal | ❌ | ✅ | ✅ | ✅ |
| Panda | ❌ | ✅ | ❌ | ❌ |
| Ridgeback | ❌ | ✅ | ❌ | ❌ |
| UR5 | ❌ | ✅ | ❌ | ✅ |

| Driver / ROS Distro (Ubuntu OS) | ROS 1 Melodic (18.04) | ROS 1 Noetic (20.04) | ROS 2 Foxy (20.04) | ROS 2 Humble (22.04)
| --- | :---: | :---: | :---: | :---: |
| RealSense Camera | ✅ | ✅ | ✅ | ✅ |
| Velodyne LiDAR | ✅ | ✅ | ✅ | ✅ |
| Robotiq 2F-85 Gripper | ✅ | ✅ | ❌ | ❌ |
| Robotiq FT-300 Force-Torque Sensor | ✅ | ✅ | ❌ | ❌ |

## Examples

### UR5 Robot
```
./run.py -n my_ur5_project -f ur5/Dockerfile.noetic
source devel/setup.bash
roslaunch ur_robot_driver ur5_bringup.launch robot_ip:=10.0.0.2
roslaunch ur5_moveit_config moveit_planning_execution.launch
roslaunch ur5_moveit_config moveit_rviz.launch
```
