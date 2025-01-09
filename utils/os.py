import os


def join_with_parent_dir(*args):
    parent_dir = get_parent_dir()
    return os.path.join(parent_dir, *args)


def get_parent_dir():
    current_dir = os.path.dirname(__file__)
    return os.path.dirname(current_dir)