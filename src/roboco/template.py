# ruff: noqa: T201
import os
import shutil

try:
    # Python < 3.9
    import importlib_resources as ilr  # type: ignore
except ImportError:
    # Python >= 3.9
    import importlib.resources as ilr
from pathlib import Path

from roboco import __version__
from roboco.configurations import ProjectConfiguration


def generate_from_template(configuration: ProjectConfiguration, destination: Path):
    dockerfile_template = f"{configuration.robot.key}/Dockerfile.{configuration.ros_distro}"
    print(f"Generating from {dockerfile_template}")
    package_dir = ilr.files("roboco")
    print(f"Package dir: {package_dir}")
    run_script_dest = destination / "run.py"
    dockerfile_dest = destination / "Dockerfile"
    run_script_src = f"{package_dir}/run.py"
    dockerfile_src = f"{package_dir}/templates/{dockerfile_template}"

    shutil.copyfile(dockerfile_src, dockerfile_dest)
    shutil.copyfile(run_script_src, run_script_dest)
    os.chmod(run_script_dest, 0o755)  # noqa: S103

    replace_string_in_file(Path(run_script_dest), "please_change_project_name", configuration.name)
    add_to_beginning_of_file(Path(dockerfile_dest), f"# Generated using roboco version {__version__}\n")


def replace_string_in_file(file: Path, old: str, new: str):
    """Removes the old string and inserts the new string in its place."""
    with open(file) as f:
        new_text = f.read().replace(old, new)
    with open(file, "w") as f:
        f.write(new_text)


def add_to_beginning_of_file(file: Path, new: str):
    """Adds the new string to the beginning of the file."""
    with open(file) as f:
        old_text = f.read()
    with open(file, "w") as f:
        f.write(new)
        f.write(old_text)
