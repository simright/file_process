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


def is_ansys_file(fpath):
    if is_ansys_fname(fpath):
        return True
    return is_ansys_file_by_content(fpath)


def is_ansys_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            if line.startswith('/PREP7') or line.startswith('/prep7'):
                return True
            if line.startswith('/solu') or line.startswith('/solu'):
                return True
            if line.startswith('/post1') or line.startswith('/post1'):
                return True
            if line.startswith('/post26') or line.startswith('/post26'):
                return True

        return False