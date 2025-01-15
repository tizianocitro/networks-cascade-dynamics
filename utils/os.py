import os


def join_with_parent_dir(*args):
    parent_dir = get_parent_dir()
    return os.path.join(parent_dir, *args)


def get_parent_dir():
    current_dir = os.path.dirname(__file__)
    return os.path.dirname(current_dir)


def str_to_bool(value: str) -> bool:
    if not value:
        return False
    return value.strip().lower() in ("true", "1", "yes", "on")