import os

from fem_utils import common_utils


def is_nastran_ext(ext):
    return ext in ['.bdf', '.nas']


def is_nastran_fname(fname):
    _, ext = os.path.splitext(fname)
    return is_nastran_ext(ext.lower())


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


def is_nastran_file(fpath):
    if is_nastran_fname(fpath):
        return True
    return is_nastran_file_by_content(fpath)


def is_nastran_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            if line.startswith('GRID') or line.startswith('grid'):
                return True
            if line.startswith('INCLUDE') or line.startswith('include'):
                line = line.strip()
                wordsInLine_list = line.split()
                if len(wordsInLine_list) > 1:
                    include_fname = wordsInLine_list[1]
                    include_fname = include_fname.strip('"')
                    include_fname = include_fname.strip("'")
                    include_fpath = os.path.join(os.path.dirname(fpath), include_fname)
                    if os.path.isfile(include_fpath):
                        if is_nastran_file_by_content(include_fpath):
                            return True
    return False

def nastran_keywords():
    return ['GRID']


if __name__ == "__main__":
    fpath = 'E:/Works/GitProject/fem_utils/tests/data/nastran(.bdf)/quad_no_ext'
    print(is_nastran_file_by_content(fpath))