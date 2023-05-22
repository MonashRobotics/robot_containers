
# Robot Containers

## Creating a new project

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

| Robots / ROS Distro (Ubuntu OS) | ROS 1 Melodic (18.04) | ROS 1 Noetic (20.04) | ROS 2 Foxy (20.04) | ROS 2 Humble (22.04)
| --- | :---: | :---: | :---: | :---: |
| ABB YuMi | ✅ | ✅ | ❌ | ❌ |
| Baxter | ❌ | ✅ | ❌ | ❌ |
| Fetch | ❌ | ✅ | ❌ | ❌ |
| Jackal | ❌ | ✅ | ✅ | ✅ |
| Panda | ❌ | ✅ | ❌ | ❌ |
| Ridgeback | ❌ | ✅ | ❌ | ❌ |
| UR5 | ❌ | ✅ | ❌ | ✅ |

## Examples

### UR5 Robot
```
./run.py -n my_ur5_project -f ur5/Dockerfile.noetic
source devel/setup.bash
roslaunch ur_robot_driver ur5_bringup.launch robot_ip:=10.0.0.2
roslaunch ur5_moveit_config moveit_planning_execution.launch
roslaunch ur5_moveit_config moveit_rviz.launch
```

### Robot-Specific Notes

#### UR5

The driver for the robotiq gripper is not available for ROS2.

### Notes on GUI/GPU support

https://github.com/osrf/rocker/tree/main/src/rocker/templates

https://github.com/dusty-nv/jetson-containers

### How to create a .repos file for use by vcstool

```
git clone https://repo-a.git
git clone https://repo-b.git
vcs export > sourcecode.repos
```