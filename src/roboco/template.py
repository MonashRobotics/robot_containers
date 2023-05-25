import os
import shutil
from pathlib import Path

from roboco.configurations import ProjectConfiguration, realsense_camera, ur5


def generate_from_template(configuration: ProjectConfiguration):
    print(f"Generating from {configuration.robot.key}")
    package_dir = Path(__file__).parent.parent.parent
    shutil.copyfile(f"{package_dir}/{configuration.robot.key}/Dockerfile.{configuration.ros_distro}", "Dockerfile")
    shutil.copyfile(f"{package_dir}/run.py", "run.py")
    os.chmod("run.py", 0o755) # noqa: S103
    
    # TODO: replace the project name
    # TODO: check for overwriting


if __name__ == "__main__":
    test_config = ProjectConfiguration("my_test_project", ur5, "noetic", [realsense_camera])
    generate_from_template(test_config)
