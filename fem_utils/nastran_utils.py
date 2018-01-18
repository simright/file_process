import os, re

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


def nastran_keywords_pattern():
    keywords_pattern = r'^(grid)|(ctria3)|(cquad4)|(chexa)|(ctera)|(mat\d)|(spc\d?)|(force\d?)|(pload\d?)'
    return keywords_pattern


def is_nastran_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            line_lower = line.strip().lower()
            if re.search(nastran_keywords_pattern(), line_lower):
                return True
            if line_lower.startswith('include'):
                return True
        return False


if __name__ == "__main__":
    fpath = 'D:/worksCode/fem_utils/tests/data/nastran(.bdf)/quad_no_ext'
    print(is_nastran_file_by_content(fpath))