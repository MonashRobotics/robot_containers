#!/usr/bin/env python3
import subprocess

image_name = "humble-base"

def attach_to_container(image_name: str):
    pass

def start_container(image_name: str):
    pass

def create_container(image_name: str):
    pass

subprocess.run(["docker", "run", "-it", "--rm", image_name])