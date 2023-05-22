#!/usr/bin/env python3
from InquirerPy import inquirer
from InquirerPy import get_style
from InquirerPy.base.control import Choice
style = get_style({"input": "#61afef", "questionmark": "#e5e512", "answermark": "#00ffa1 bold"}, style_override=False)
tick = u'\u2714'

# This template makes heavy use of https://inquirerpy.readthedocs.io/en/latest/

from dataclasses import dataclass

@dataclass
class HardwareAddition:
    short_name: str
    long_name: str
    supported_ros_versions: list[str]

@dataclass
class Robot:
    short_name: str
    long_name: str
    supported_ros_versions: list[str]

hardware_names = {
    "realsense_camera": "RealSense Camera",
    "robotiq_gripper": "Robotiq 2F-85 Gripper",
    "robotiq_force_torque": "Robotiq FT-300 Force-Torque Sensor",
    "papillarray": "Contactile Papillarray Tactile Sensor",
}

robot_names = {
    "abb_yumi": "ABB YuMi",
    "baxter": "Baxter",
    "fetch": "Fetch",
    "jackal": "Jackal",
    "panda": "Panda",
    "ridgeback": "Ridgeback",
    "ur5": "UR5",
    "other": "Other",
}

ros_versions_by_robot = {
    "abb_yumi": ["melodic", "noetic"],
    "baxter": ["kinetic", "noetic"],
    "fetch": ["melodic", "noetic"],
    "jackal": ["noetic", "foxy", "humble"],
    "panda": ["melodic", "noetic"],
    "ridgeback": ["noetic"],
    "ur5": ["melodic", "noetic", "humble"],
    "other": ["melodic", "noetic", "foxy", "humble"],
}

ros_versions_by_sensor = {
    "realsense_camera": ["melodic", "noetic", "foxy", "humble"],
    "robotiq_gripper": ["melodic", "noetic", "foxy", "humble"],
    "robotiq_force_torque": ["melodic", "noetic", "foxy", "humble"],
    "papillarray": ["melodic", "noetic", "foxy", "humble"],
}

name = inquirer.text(message="Project name:", style=style, amark=tick).execute()
robot = inquirer.select(
    message="Choose your robot:",
    choices=[Choice(key, value) for key, value in robot_names.items()],
    style=style,
    amark=tick
).execute()

ros_distro = inquirer.select("ROS version:", choices=ros_versions_by_robot[robot], style=style, amark=tick).execute()

hardware_options_by_robot = {
    "abb_yumi": [],
    "baxter": [],
    "fetch": [],
    "jackal": [],
    "panda": [],
    "ridgeback": [],
    "ur5": [
        "realsense_camera",
        "robotiq_gripper",
        "robotiq_force_torque",
        "papillarray",
    ],
    "other": [],
}

possible_hardware_options = [option for option in hardware_options_by_robot[robot] if ros_distro in ros_versions_by_sensor[option]]
possible_hardware_options = [Choice(key, hardware_names[key]) for key in possible_hardware_options]

if len(possible_hardware_options) > 0:
    hardware = inquirer.checkbox("Additional hardware: (space to toggle selection)", choices=possible_hardware_options, style=style, amark=tick).execute()

confirm = inquirer.confirm(message="Create project?", style=style, amark=tick).execute()

if not confirm:
    print("Cancelled.")
    quit()

print(f"\nCreating project...")

print(f"\nDone. Now run: ")
print(f"""
    cd {name}
    ./run.py
""")