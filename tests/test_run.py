import logging
from pathlib import Path

from roboco.run import build_image


def test_build_image():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    build_successful = build_image("test", "tests/Dockerfile.minimal", Path("."))
    assert build_successful
