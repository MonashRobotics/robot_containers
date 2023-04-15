#!/usr/bin/env python3
import subprocess
import argparse

image_name = "humble-base"
dockerfile = "Dockerfile.ros2"


def build_container(image_name: str, dockerfile: str):
    subprocess.run(["docker", "build", ".", "-f", dockerfile, "-t", image_name])


if __name__ == "__main__":
    build_container(image_name, dockerfile)