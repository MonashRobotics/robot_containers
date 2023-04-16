#!/usr/bin/env python3
import argparse
import subprocess

image_name = "humble-base"

def attach_to_container(image_name: str):
    pass

def start_container(image_name: str):
    pass

def create_container(image_name: str):
    pass

def run_container(image_name: str):
    subprocess.run(["docker", "run", "-it", "--rm", image_name])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Builder',
        description='Builds docker images',
        epilog='Text at the bottom of help')
    parser.add_argument('robot')
    args = parser.parse_args()

    image_name = args.robot

    print(f"Running {image_name} image")
    run_container(image_name)