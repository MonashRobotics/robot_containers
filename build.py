#!/usr/bin/env python3
""" Script to make it easier to build images from the included Dockerfiles """
import argparse
import subprocess

robot_dockerfiles = {
    "baxter-kinetic": "baxter/Dockerfile.kinetic",
    "baxter-noetic": "baxter/Dockerfile.noetic",
    "pepper-kinetic": "pepper/Dockerfile.kinetic",
    "pepper-noetic": "pepper/Dockerfile.noetic",
    "abb_yumi-melodic": "abb_yumi/Dockerfile.melodic",
    "abb_yumi-noetic": "abb_yumi/Dockerfile.noetic",
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