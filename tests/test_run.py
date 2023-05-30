import logging
from pathlib import Path

from roboco.configurations import ProjectConfiguration, realsense_camera, ur5
from roboco.run import attach_to_container, build_image, create_container, remove_container, remove_image


def test_build_image():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    build_successful = build_image("test", "tests/Dockerfile.minimal", Path("."))
    assert build_successful

# def test_create_container():
#     log = logging.getLogger()
#     log.setLevel(logging.DEBUG)
#     create_successful = create_container("test", "test")
#     assert create_successful
