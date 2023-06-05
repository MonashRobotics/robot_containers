import logging
from pathlib import Path

from roboco.run import build_image, remove_image


def test_build_image():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    build_image("test", "tests/Dockerfile.minimal", Path("."))


def test_remove_image():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    build_image("test", "tests/Dockerfile.minimal", Path("."))
    remove_image("test")
