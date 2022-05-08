from subprocess import run
from pathlib import Path

from dogebuild import make_mode, task


make_mode()

IMAGE_NAME = "vault-13-fomo-bot"
BUILD_DIR = Path("./build")


@task
def build_docker():
    run(["docker", "build", "-t", IMAGE_NAME, "."], check=True)


@task(depends=["build_docker"])
def run_docker():
    run(["docker", "run", IMAGE_NAME], check=True)


@task(depends=["build_docker"])
def build_tar():
    BUILD_DIR.mkdir(exist_ok=True)
    run(["docker", "save", "--output", f"{BUILD_DIR / (IMAGE_NAME + '.tar')}", IMAGE_NAME])
