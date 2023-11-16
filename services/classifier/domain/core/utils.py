import os
from pathlib import Path


def get_project_root():
    return Path(__file__).parent.parent.parent


def get_env_path():
    return os.path.join(get_project_root(), ".env")


def get_path_from_root(custom_path: str):
    return os.path.join(get_project_root(), custom_path)
