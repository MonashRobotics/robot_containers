#!/usr/bin/env python3
# ruff: noqa: T201 S602
""" Script to make it easier to build and run a container"""
import argparse
import subprocess
import sys
from pathlib import Path

# Default values when no arguments are provided.
PROJECT_NAME = "please_change_project_name"
DOCKERFILE = "./Dockerfile"


def build_image(image_name: str, dockerfile: str):
    """
    Build an image from the supplied dockerfile.

    Uses the current directory as the docker context.
    """
    dockerfile_exists = Path(dockerfile).exists()
    if not dockerfile_exists:
        print(f"Error: {dockerfile} does not exist.")
        sys.exit()
    build_command = f"docker build . -f {dockerfile} -t {image_name}"
    subprocess.run(build_command, shell=True)


def create_container(image_name: str, container_name: str):
    """
    Use 'docker run' to create a container.

    - GUI application support is enabled by setting the DISPLAY environment variable,
    and sharing the .X11-unix socket as a volume.
    - External device support is enabled by sharing /dev as a volume.
    - Full networking support is enabled by setting network mode to 'host' and
    enabling the 'privileged' flag.
    - Loading of kernel modules from inside the container is enabled by sharing
    /lib/modules as a volume.
    - Realtime scheduling support is enabled by setting ulimits
    - The ROS distro is sourced by the ros_entrypoint.sh script supplied in the
    upstream docker images.
    - The current working directory is shared as a volume inside the container.
    - The container is started in the background, so that we can later attach
    to it from multiple terminals using 'docker exec'.
    """
    run_command = f"""docker run -it \
        -e DISPLAY \
        --volume "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        --network=host \
        --privileged \
        --volume "/dev:/dev:rw" \
        --volume "/lib/modules:/lib/modules:rw" \
        --ulimit rtprio=99 \
        --ulimit rttime=-1 \
        --ulimit memlock=8428281856 \
        --entrypoint /ros_entrypoint.sh \
        --volume "$(pwd):/home/roboco/ros_ws/src/{PROJECT_NAME}" \
        --name {container_name} \
        -d {image_name} \
        /usr/bin/tail -f /dev/null
    """
    print(run_command)
    subprocess.run(run_command, shell=True)


def attach_to_container(container_name: str):
    """
    Attach the terminal to an existing container, starting it if it is currently in
    stopped state.
    """
    # Allow container to create GUI windows on the host's X server
    subprocess.run("xhost + >> /dev/null", shell=True)  # noqa: S607
    # Start the container in case it has been stopped
    subprocess.run(f"docker start {container_name}", shell=True)
    # Attach a terminal into the container
    starting_command = "bash"  # you can edit this if you wish. e.g. bash -c ~/project/tmux_start.sh
    subprocess.run(f"docker exec -it {container_name} {starting_command}", shell=True)


def remove_container(container_name: str):
    """Delete the container."""
    remove_container_command = f"docker rm -f {container_name}"
    print(remove_container_command)
    subprocess.run(remove_container_command, shell=True)


def remove_image(image_name: str):
    """Delete the image."""
    remove_image_command = f"docker rmi -f {image_name}"
    print(remove_image_command)
    subprocess.run(remove_image_command, shell=True)


def image_exists(image_name: str) -> bool:
    """Check if an image with the specified name has previously been built"""
    image_list_command = f"docker images -f reference=^/{image_name}$ -q"
    output = subprocess.run(
        image_list_command, stdout=subprocess.PIPE, shell=True
    ).stdout.decode()  # run the command as if in a shell, capture stdout
    already_exists = len(output) > 0
    return already_exists


def container_exists(container_name: str) -> bool:
    """
    Check if an image with the specified name has previously been created.

    It can be in stopped or running state.
    """
    container_list_command = f"docker ps -qa -f name=^/{container_name}$"
    output = subprocess.run(
        container_list_command, stdout=subprocess.PIPE, shell=True
    ).stdout.decode()  # run the command as if in a shell, capture stdout
    already_exists = len(output) > 0
    return already_exists


def main(args: argparse.Namespace):
    min_container_name_length = 2
    if not args.name or len(args.name) < min_container_name_length:
        print("Error. Please provide a non-empty project name of at least 2 characters.")
        sys.exit()
    project_name = args.name
    dockerfile = args.file
    force_rebuild = args.rebuild
    should_remove_container = args.rm
    should_remove_image = args.rmi

    if should_remove_container:
        remove_container(project_name)
        sys.exit()

    if should_remove_image:
        remove_image(project_name)
        sys.exit()

    if force_rebuild or not image_exists(project_name):
        build_image(project_name, dockerfile)

    if not container_exists(project_name):
        create_container(project_name, project_name)

    attach_to_container(project_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs docker containers")
    parser.add_argument(
        "-n",
        "--name",
        default=PROJECT_NAME,
        help="name of project (used to name image and container)",
    )
    parser.add_argument(
        "-f",
        "--file",
        default=DOCKERFILE,
        help="""dockerfile from which to build an image (if the image isn't already
built)""",
    )
    parser.add_argument(
        "-r",
        "--rebuild",
        action="store_true",
        help="force a rebuild of the docker image",
    )
    parser.add_argument("--rm", "--remove-container", action="store_true", help="delete the container")
    parser.add_argument("--rmi", "--remove-image", action="store_true", help="delete the image")
    args = parser.parse_args()

    main(args)
