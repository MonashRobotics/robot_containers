#!/usr/bin/env python3
""" Script to make it easier to build and run a container"""
import argparse
import subprocess

# Default values when no arguments are provided.
PROJECT_NAME="ur5-noetic"
DOCKERFILE="ur5/Dockerfile.noetic"

def build_image(image_name: str, dockerfile: str):
    subprocess.run(["docker", "build", ".", "-f", dockerfile, "-t", image_name])

def create_container(image_name: str):
    run_command = f"""docker run -it \
        -e DISPLAY \
        --volume "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        --network=host \
        --volume "/dev:/dev:rw" \
        --volume "/lib/modules:/lib/modules:rw" \
        --ulimit rtprio=99 \
        --ulimit rttime=-1 \
        --ulimit memlock=8428281856 \
        --entrypoint /ros_entrypoint.sh \
        --volume "$(pwd):/home/roboco/ros_ws/src/{PROJECT_NAME}" \
        --name {image_name} \
        -d {image_name} \
        /usr/bin/tail -f /dev/null
    """
    print(run_command)
    subprocess.run(run_command, shell=True)

def attach_to_container(container_name: str):
    # Allow container to create GUI windows on the host's X server
    subprocess.run("xhost + >> /dev/null", shell=True)
    # Start the container in case it has been stopped
    subprocess.run(f"docker start {container_name}", shell=True)
    # Attach a terminal into the container
    starting_command = "bash" # you can edit this if you wish. e.g. bash -c ~/project/tmux_start.sh
    subprocess.run(f"docker exec -it {container_name} {starting_command}", shell=True)

def image_exists(image_name: str) -> bool:
    image_list_command = f"docker images -f reference={image_name} -q"
    output = subprocess.run(image_list_command, stdout=subprocess.PIPE, shell=True).stdout.decode() # run the command as if in a shell, capture stdout
    already_exists = len(output) > 0
    return already_exists

def container_exists(container_name: str) -> bool:
    container_list_command = f"docker ps -qa -f name={image_name}"
    output = subprocess.run(container_list_command, stdout=subprocess.PIPE, shell=True).stdout.decode() # run the command as if in a shell, capture stdout
    already_exists = len(output) > 0
    return already_exists

def main(project_name: str, dockerfile: str, force_rebuild: bool):
    if force_rebuild or not image_exists(project_name):
        build_image(project_name, dockerfile)

    if not container_exists(project_name):
        create_container(project_name)
        
    attach_to_container(project_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs docker containers')
    parser.add_argument('-n', '--name', default=PROJECT_NAME, help='name of project (used to name image and container)')
    parser.add_argument('-f', '--file', default=DOCKERFILE, help="dockerfile from which to build an image (if the image isn't already built)")
    parser.add_argument('-r', '--rebuild', action='store_true', help="force a rebuild of the docker image")
    args = parser.parse_args()

    image_name = args.name
    docker_file = args.file
    rebuild = args.rebuild
    
    main(image_name, docker_file, rebuild)  
    