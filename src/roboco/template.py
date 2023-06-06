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

from InquirerPy.utils import color_print

from roboco import __version__
from roboco.configurations import HardwareOption, ProjectConfiguration
from roboco.printing import orange, yellow


def generate_from_template(configuration: ProjectConfiguration, destination: Path):
    dockerfile_template = f"{configuration.robot.key}/Dockerfile.{configuration.ros_distro}"
    print(f"Generating from {dockerfile_template}")
    package_dir = ilr.files("roboco")
    run_script_dest = destination / "run.py"
    dockerfile_dest = destination / "Dockerfile"
    run_script_src = f"{package_dir}/run.py"
    dockerfile_src = f"{package_dir}/templates/{dockerfile_template}"

    shutil.copyfile(dockerfile_src, dockerfile_dest)
    shutil.copyfile(run_script_src, run_script_dest)
    os.chmod(run_script_dest, 0o755)  # noqa: S103

    # Replace placeholders in the run script and Dockerfile
    replace_string_in_file(Path(run_script_dest), "please_change_project_name", configuration.name)
    add_to_beginning_of_file(Path(dockerfile_dest), f"# Generated using roboco version {__version__}\n")

    # Insert selected snippets and preamble into the Dockerfile
    snippet_string = concatenate_snippets(configuration)
    preamble_string = concatenate_preambles(configuration)
    replace_string_in_file(Path(dockerfile_dest), "# SNIPPETS_SECTION_START\n# SNIPPETS_SECTION_END", snippet_string)
    replace_string_in_file(Path(dockerfile_dest), "# PREAMBLE_SECTION_START\n# PREAMBLE_SECTION_END", preamble_string)


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


def concatenate_snippets(configuration: ProjectConfiguration) -> str:
    package_dir = ilr.files("roboco")
    snippets = ["# SNIPPETS_SECTION_START"]
    for addition in configuration.hardware:
        snippet_src = f"{package_dir}/snippets/Dockerfile.{addition.key}.snippet"
        with open(snippet_src) as f:
            snippet_contents = f.read()
            snippets.append(snippet_contents)
    snippets.append("# SNIPPETS_SECTION_END")
    concatenated_snippets = "\n\n".join(snippets)
    return concatenated_snippets


def concatenate_preambles(configuration: ProjectConfiguration) -> str:
    package_dir = ilr.files("roboco")
    preambles = ["# PREAMBLE_SECTION_START"]
    for addition in configuration.hardware:
        if addition.has_preamble:
            snippet_src = f"{package_dir}/snippets/Dockerfile.{addition.key}.preamble"
            with open(snippet_src) as f:
                snippet_contents = f.read()
                preambles.append(snippet_contents)
    preambles.append("# PREAMBLE_SECTION_END")
    concatenated_preambles = "\n\n".join(preambles)
    return concatenated_preambles


def display_snippets(additional_options: list[HardwareOption]):
    package_dir = ilr.files("roboco")
    for addition in additional_options:
        print(f"\n{addition.name}")
        if addition.has_preamble:
            preamble_src = f"{package_dir}/snippets/Dockerfile.{addition.key}.preamble"
            with open(preamble_src) as f:
                preamble_contents = f.read()
                msg = """\nAdd the following preamble to the top of your Dockerfile
(marked as PREAMBLE_SECTION_START/END):\n"""
                color_print([(yellow, msg)])
                color_print([(orange, preamble_contents)])

        snippet_src = f"{package_dir}/snippets/Dockerfile.{addition.key}.snippet"
        with open(snippet_src) as f:
            snippet_contents = f.read()
            msg = """\nAdd the following snippet to the middle of your Dockerfile
(marked as SNIPPETS_SECTION_START/END):\n"""
            color_print([(yellow, msg)])
            color_print([(orange, snippet_contents)])
