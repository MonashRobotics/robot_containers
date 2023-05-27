#!/usr/bin/env python3
# ruff: noqa: T201 S602
""" Script to make it easier to build and run a container"""
import argparse
import logging
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
        log.error(f"Error: {dockerfile} does not exist.")
        sys.exit()
    build_command = f"docker build . -f {dockerfile} -t {image_name}"
    log.debug(build_command)
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
        -it {image_name} \
        bash
    """
    log.info(run_command)
    subprocess.run(run_command, shell=True)


def attach_to_container(container_name: str):
    """
    Attach the terminal to an existing container, starting it if it is currently in
    stopped state.
    """
    # Allow container to create GUI windows on the host's X server
    subprocess.run("xhost + >> /dev/null", shell=True)
    # Start the container in case it has been stopped
    start_command = f"docker start {container_name}"
    log.info(start_command)
    subprocess.run(start_command, shell=True)
    # Attach a terminal into the container
    program_to_run = "bash"  # you can edit this if you wish. e.g. bash -c ~/project/tmux_start.sh
    attach_command = f"docker exec -it {container_name} {program_to_run}"
    log.info(attach_command)
    subprocess.run(attach_command, shell=True)


def remove_container(container_name: str):
    """Delete the container."""
    remove_container_command = f"docker rm -f {container_name}"
    log.info(remove_container_command)
    subprocess.run(remove_container_command, shell=True)


def remove_image(image_name: str):
    """Delete the image."""
    remove_image_command = f"docker rmi -f {image_name}"
    log.info(remove_image_command)
    subprocess.run(remove_image_command, shell=True)


def image_exists(image_name: str) -> bool:
    """Check if an image with the specified name has previously been built"""
    image_list_command = f"docker images -f reference={image_name} -q"
    log.debug(image_list_command)
    output = subprocess.run(
        image_list_command, stdout=subprocess.PIPE, shell=True
    ).stdout.decode()  # run the command as if in a shell, capture stdout
    log.debug(output)
    already_exists = len(output) > 0
    return already_exists


def container_exists(container_name: str) -> bool:
    """
    Check if an image with the specified name has previously been created.

    It can be in stopped or running state.
    """
    # regex used to filter containers by exact name, rather than just substring
    container_list_command = f"docker ps -qa --no-trunc -f name=^/{container_name}$"
    log.debug(container_list_command)
    output = subprocess.run(
        container_list_command, stdout=subprocess.PIPE, shell=True
    ).stdout.decode()  # run the command as if in a shell, capture stdout
    log.debug(output)
    already_exists = len(output) > 0
    return already_exists


def shell():
    """Run a shell inside the container."""
    if not image_exists(PROJECT_NAME):
        build_image(PROJECT_NAME, DOCKERFILE)

    if not container_exists(PROJECT_NAME):
        create_container(PROJECT_NAME, PROJECT_NAME)
    else:
        attach_to_container(PROJECT_NAME)


def build():
    build_image(PROJECT_NAME, DOCKERFILE)


def rm():
    remove_container(PROJECT_NAME)


def rmi():
    remove_image(PROJECT_NAME)


def main(args: argparse.Namespace):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs docker containers")
    subparsers = parser.add_subparsers(help="sub-command help")
    parser_shell = subparsers.add_parser(
        "shell", help="run a shell inside a docker container, building and starting it if necessary"
    )
    parser_shell.set_defaults(func=shell)
    parser_build = subparsers.add_parser("build", help="build a docker image")
    parser_build.set_defaults(func=build)
    parser_rm = subparsers.add_parser("rm", help="remove a docker container")
    parser_rm.set_defaults(func=rm)
    parser_rmi = subparsers.add_parser("rmi", help="remove a docker image")
    parser_rmi.set_defaults(func=rmi)
    parser.add_argument("--verbose", action="store_true", help="print debug messages")

    log = logging.getLogger()
    min_container_name_length = 2
    if len(PROJECT_NAME) < min_container_name_length:
        log.error(
            f"Error. Project name '{PROJECT_NAME}' is too short."
            "Please provide a non-empty project name of at least 2 characters."
        )
        sys.exit()

    args = parser.parse_args()
    print(args)
    args.func(args)

    # main(args )
