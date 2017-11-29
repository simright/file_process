import os

from fem_utils import common_utils


def is_abaqus_ext(ext):
    return ext in ['.inp']


def is_abaqus_fname(fname):
    _, ext = os.path.splitext(fname)
    return is_abaqus_ext(ext.lower())


def get_include_files(fpath):
    include_files = list()

    basedir = os.path.dirname(fpath)
    with open(fpath, 'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break

            if line.startswith('*INCLUDE'):
                fields = line.split(',')
                if len(fields) > 1:
                    item = fields[-1].split('=')[-1].strip()
                    include_files.append(common_utils.get_abspath(basedir, item))

    return include_files
