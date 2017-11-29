import os


def get_abspath(basedir, path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(os.path.join(basedir, path))
