#!/usr/bin/env python3
""" Script to make it easier to build and run containers from the images in this repo """
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

def attach_to_container(image_name: str):
    # docker exec -it container_name bash
    pass

def start_container(image_name: str):
    pass

def create_container(image_name: str):
    pass

def run_container(image_name: str):
    run_command = f"""docker run -it \
        --rm \
        --network=host \
        --ulimit rtprio=99 \
        --ulimit rttime=-1 \
        --ulimit memlock=8428281856 \
        {image_name}
    """
    print(run_command)
    subprocess.run(run_command, shell=True)

def image_exists(image_name: str) -> bool:
    image_list_command = f"docker images -f reference={image_name} -q"
    result = subprocess.run(image_list_command, stdout=subprocess.PIPE, shell=True) # run the command as if in a shell, capture stdout
    output = result.stdout.decode()
    already_exists = len(output) > 0
    return already_exists

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs docker containers')
    parser.add_argument('robot', choices=robot_dockerfiles.keys())
    args = parser.parse_args()

    image_name = args.robot

    if not image_exists(image_name):
        # attempt to build
        build_container(image_name, robot_dockerfiles[image_name])

    run_container(image_name)