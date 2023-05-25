import shutil

from roboco.configurations import ProjectConfiguration, realsense_camera, ur5


def generate_from_template(configuration: ProjectConfiguration):
    print(configuration.robot.key)


if __name__ == "__main__":
    test_config = ProjectConfiguration("my_test_project", ur5, "noetic", [realsense_camera])
    generate_from_template(test_config)
