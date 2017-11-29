import os

from fem_utils import common_utils


def is_optistruct_ext(ext):
    return ext in ['.fem']


def is_optistruct_fname(fname):
    _, ext = os.path.splitext(fname)
    return is_optistruct_ext(ext.lower())


def get_include_files(fpath):
    include_files = list()

    basedir = os.path.dirname(fpath)
    with open(fpath, 'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            if line.startswith('INCLUDE') or line.startswith('include'):
                line = line.strip()
                fields = line.split(' ')
                if len(fields) > 1:
                    item = fields[1]
                    item = item.strip("'")
                    item = item.strip('"')
                    include_files.append(common_utils.get_abspath(basedir, item))

    return include_files
