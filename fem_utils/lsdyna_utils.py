import os

from fem_utils import common_utils


def is_lsdyna_ext(ext):
    return ext in ['.k', '.key', '.dyn']


def is_lsdyna_fname(fname):
    _, ext = os.path.splitext(fname)
    return is_lsdyna_ext(ext.lower())


def get_include_files(fpath):
    include_files = list()

    basedir = os.path.dirname(fpath)
    with open(fpath, 'r') as fp:
        line_process_switch = False
        while 1:
            line = fp.readline()
            if not line:
                break

            line = line.strip()
            line_upper = line.upper()
            if line_upper.startswith('*INCLUDE'):
                line_process_switch = True
            elif line_upper.startswith('*'):
                line_process_switch = False

            if line_process_switch and not line.startswith('*'):
                fname = line.strip()
                include_files.append(common_utils.get_abspath(basedir, fname))

    return include_files
