#!/usr/bin/env python3
""" Script to make it easier to build images from the included Dockerfiles """
import argparse
import subprocess

robot_dockerfiles = {
    "baxter-kinetic": "baxter/Dockerfile.kinetic",
    "baxter-noetic": "baxter/Dockerfile.noetic",
    "abb_yumi-melodic": "abb_yumi/Dockerfile.melodic",
    "abb_yumi-noetic": "abb_yumi/Dockerfile.noetic",
    "fetch-melodic": "fetch/Dockerfile.melodic",
    "fetch-noetic": "fetch/Dockerfile.noetic",
    "jackal-noetic": "jackal/Dockerfile.noetic",
    "jackal-foxy": "jackal/Dockerfile.foxy",
    "jackal-humble": "jackal/Dockerfile.humble",
    "ur5-noetic": "ur5/Dockerfile.noetic",
    "ur5-humble": "ur5/Dockerfile.humble",
    "ridgeback-noetic": "ridgeback/Dockerfile.noetic",
}

def build_container(image_name: str, dockerfile: str):
    subprocess.run(["docker", "build", ".", "-f", dockerfile, "-t", image_name])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Builds docker images')
    parser.add_argument('robot', choices=robot_dockerfiles.keys())
    args = parser.parse_args()

    dockerfile = robot_dockerfiles[args.robot]

    print(f"Building {args.robot} image from {dockerfile}")
    build_container(args.robot, dockerfile)