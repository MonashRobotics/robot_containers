#!/usr/bin/env python3
""" Script to make it easier to run containers from the images in this repo """
import argparse
import subprocess

def attach_to_container(image_name: str):
    pass

def start_container(image_name: str):
    pass

def create_container(image_name: str):
    pass

def run_container(image_name: str):
    subprocess.run(["docker", "run", "-it", "--rm", image_name])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs docker containers')
    parser.add_argument('robot')
    args = parser.parse_args()

    image_name = args.robot

    print(f"Running {image_name} image")
    run_container(image_name)