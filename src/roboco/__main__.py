#!/usr/bin/env python3
# ruff: noqa: T201
import sys
from dataclasses import dataclass
from typing import Literal

from InquirerPy import get_style, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print

ROSDistro = Literal["kinetic", "melodic", "noetic", "foxy", "humble"]


@dataclass
class HardwareOption:
    name: str
    compatible_ros_distros: list[ROSDistro]


@dataclass
class Robot:
    name: str
    compatible_ros_distros: list[ROSDistro]
    compatible_hardware: list[HardwareOption]


@dataclass
class ProjectConfiguration:
    name: str
    robot: Robot
    ros_distro: ROSDistro
    hardware: list[HardwareOption]


green = "#00ffa1"
red = "#ff5858"
style = get_style(
    {"input": "#61afef", "questionmark": "#e5e512", "answermark": f"{green} bold"},
    style_override=False,
)
tick = "\u2714"

# This template makes heavy use of https://inquirerpy.readthedocs.io/en/latest/

realsense_camera = HardwareOption("RealSense Camera", ["melodic", "noetic", "foxy", "humble"])
robotiq_gripper = HardwareOption("Robotiq 2F-85 Gripper", ["melodic", "noetic"])
robotiq_force_torque = HardwareOption("Robotiq FT-300 Force-Torque Sensor", ["melodic", "noetic"])
papillarray = HardwareOption("Contactile Papillarray Tactile Sensor", ["melodic", "noetic"])

abb_yumi = Robot("ABB YuMi", ["melodic", "noetic"], [])
baxter = Robot("Baxter", ["kinetic", "noetic"], [])
fetch = Robot("Fetch", ["melodic", "noetic"], [])
jackal = Robot("Jackal", ["noetic", "foxy", "humble"], [realsense_camera])
panda = Robot("Panda", ["melodic", "noetic"], [realsense_camera])
ridgeback = Robot("Ridgeback", ["noetic"], [])
ur5 = Robot(
    "UR5", ["melodic", "noetic", "humble"], [realsense_camera, robotiq_gripper, robotiq_force_torque, papillarray]
)
other = Robot("Other", ["melodic", "noetic", "foxy", "humble"], [])

robots = [abb_yumi, baxter, fetch, jackal, panda, ridgeback, ur5, other]


def main():
    name = inquirer.text(message="Project name:", style=style, amark=tick).execute()
    if not name:
        print("Please enter a non-empty name.")
        sys.exit()

    robot_choice = inquirer.select(
        message="Choose your robot:",
        choices=[Choice(robot, robot.name) for robot in robots],
        style=style,
        amark=tick,
    ).execute()

    ros_distro = inquirer.select(
        "ROS version:", choices=robot_choice["compatible_ros_distros"], style=style, amark=tick
    ).execute()

    possible_hardware_options = [
        Choice(hardware_option, hardware_option["name"]) for hardware_option in robot_choice["compatible_hardware"]
    ]

    hardware = []

    if len(possible_hardware_options) > 0:
        hardware = inquirer.checkbox(
            "Additional hardware:",
            instruction="(space to toggle selection)",
            choices=possible_hardware_options,
            style=style,
            amark=tick,
        ).execute()
        incompatible_hardware = False
        for hardware_option in hardware:
            if ros_distro not in hardware_option["compatible_ros_distros"]:
                incompatible_hardware = True
                error_message = f"Error: {hardware_option['name']} is not compatible with ROS {ros_distro}."
                color_print([(red, error_message)])
                print("Please choose a different ROS version or remove this hardware option and try again.")
        if incompatible_hardware:
            sys.exit()

    confirm = inquirer.confirm(message="Create project?", default=True, style=style, amark=tick).execute()

    if not confirm:
        print("Cancelled.")
        sys.exit()

    # configuration = ProjectConfiguration(name, robot_choice, ros_distro, hardware)

    print("\nCreating project...")

    color_print([(green, "\nDone. "), ("", "Now run:")])
    print(
        f"""
        cd {name}
        ./run.py
    """
    )


if __name__ == "__main__":
    main()
