#!/usr/bin/env python3
import argparse
import subprocess

image_name = "humble-base"
dockerfile = "Dockerfile.ros2"

robot_dockerfiles = {
    "baxter-kinetic": "baxter/Dockerfile.kinetic",
    "baxter-noetic": "baxter/Dockerfile.noetic",
}


def build_container(image_name: str, dockerfile: str):
    subprocess.run(["docker", "build", ".", "-f", dockerfile, "-t", image_name])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Builder',
        description='Builds docker images',
        epilog='Text at the bottom of help')
    parser.add_argument('robot')
    args = parser.parse_args()

    dockerfile = robot_dockerfiles[args.robot]

    print(f"Building {args.robot} image from {dockerfile}")
    build_container(args.robot, dockerfile)