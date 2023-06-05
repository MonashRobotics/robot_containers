
# Troubleshooting

## Installing roboco

### Problem: pip install fails
`pip install roboco` fails with an error such as the following:
```
Could not find a version that satisfies the requirement roboco (from versions: )
No matching distribution found for roboco
```

### Solution

If you are on python 3.6 or below, see [#problem-old-python-version](#problem-old-python-version).

If you are on python 3.7 or above, this may be because you are using an old version of pip. Try upgrading pip using `pip install --upgrade pip`.

### Problem: Old Python Version
If you are on python 3.6 or below, you cannot install `roboco` to guide you through creating a new container, but you can still use the Dockerfile templates. 

### Solution
Download the template you want to use from [src/roboco/templates](../src/roboco/templates/) and rename it to `Dockerfile`, download [src/roboco/run.py](../src/roboco/run.py), and place these both in your project.

Edit run.py to include a name for your project:

```python
10 # Configuration. Change these to suit your project.
11 PROJECT_NAME = "please_change_project_name"
```

Add executable permissions to run.py:

```bash
chmod +x ./run.py
```

Now you can build and run the container:

```bash
./run.py
```

## Building images

### Problem: apt-get update fails
`apt-get update` fails with an error message like 
```
Get:2 http://packages.ros.org/ros/ubuntu focal InRelease [4679 B]
#5 1.232 Err:2 http://packages.ros.org/ros/ubuntu focal InRelease
#5 1.232   At least one invalid signature was encountered.
```
### Solution
1. Download the newest docker image for your ROS distro. E.g. `docker pull osrf/ros:noetic-desktop-full`
2. If that does not fix the issue, try running `docker system prune` to free up space allocated to docker. https://stackoverflow.com/questions/59139453/repository-is-not-signed-in-docker-build