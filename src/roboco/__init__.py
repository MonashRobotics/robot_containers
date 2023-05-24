#!/usr/bin/env python3
from InquirerPy import inquirer
from InquirerPy import get_style
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print

style = get_style(
    {"input": "#61afef", "questionmark": "#e5e512", "answermark": "#00ffa1 bold"},
    style_override=False,
)
tick = "\u2714"

# This template makes heavy use of https://inquirerpy.readthedocs.io/en/latest/

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

ros_versions_by_hardware = {
    "realsense_camera": ["melodic", "noetic", "foxy", "humble"],
    "robotiq_gripper": ["melodic", "noetic"],
    "robotiq_force_torque": ["melodic", "noetic"],
    "papillarray": ["melodic", "noetic"],
}

hardware_options_by_robot: dict[str, list[str]] = {
    "abb_yumi": [],
    "baxter": [],
    "fetch": [],
    "jackal": ["realsense_camera"],
    "panda": ["realsense_camera"],
    "ridgeback": [],
    "ur5": [
        "realsense_camera",
        "robotiq_gripper",
        "robotiq_force_torque",
        "papillarray",
    ],
    "other": [],
}

def main():
    name = inquirer.text(message="Project name:", style=style, amark=tick).execute()
    robot = inquirer.select(
        message="Choose your robot:",
        choices=[Choice(key, value) for key, value in robot_names.items()],
        style=style,
        amark=tick,
    ).execute()

    ros_distro = inquirer.select(
        "ROS version:", choices=ros_versions_by_robot[robot], style=style, amark=tick
    ).execute()

    possible_hardware_options = [
        Choice(key, hardware_names[key]) for key in hardware_options_by_robot[robot]
    ]

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
            if ros_distro not in ros_versions_by_hardware[hardware_option]:
                incompatible_hardware = True
                color_print(
                    [
                        (
                            "#ff5858",
                            f"""Error: {hardware_names[hardware_option]} is not compatible 
    with ROS {ros_distro}.""",
                        )
                    ]
                )
                print(
                    """Please choose a different ROS version or remove this hardware 
    option and try again."""
                )
        if incompatible_hardware:
            quit()

    confirm = inquirer.confirm(
        message="Create project?", default=True, style=style, amark=tick
    ).execute()

    if not confirm:
        print("Cancelled.")
        quit()

    print("\nCreating project...")

    color_print([("#00ffa1", "\nDone. "), ("", "Now run:")])
    print(
        f"""
        cd {name}
        ./run.py
    """
    )

if __name__ == "__main__":
    main()