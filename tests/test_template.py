import os

from roboco.configurations import ProjectConfiguration, realsense_camera, ur5
from roboco.template import generate_from_template


def test_generate_from_template(tmpdir):
    generate_from_template(ProjectConfiguration("my_test_project", ur5, "noetic", [realsense_camera]), tmpdir)
    dockerfile_exists = os.path.exists(tmpdir / "Dockerfile")
    assert dockerfile_exists
    run_script_exists = os.path.exists(tmpdir / "run.py")
    assert run_script_exists
