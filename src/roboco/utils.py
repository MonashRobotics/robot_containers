import docker


def check_docker_image_exists(image_name: str):
    client = docker.from_env()
    try:
        print("Downloading image....")
        client.images.pull(image_name)
        return True
    except docker.errors.ImageNotFound:
        return False
