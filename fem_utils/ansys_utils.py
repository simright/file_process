import os

from fem_utils import common_utils


def is_ansys_ext(ext):
    return ext in ['.cdb']


def is_ansys_fname(fname):
    _, ext = os.path.splitext(fname)
    return is_ansys_ext(ext.lower())


def get_include_files(fpath):
    include_files = list()
    return include_files
