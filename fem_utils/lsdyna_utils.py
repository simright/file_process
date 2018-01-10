import os, re

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


def is_lsdyna_file(fpath):
    if is_lsdyna_fname(fpath):
        return True
    return is_lsdyna_file_by_content(fpath)


def is_lsdyna_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            if line.startswith('*NODE') or line.startswith('*node'):
                # compare the following five lines, because ls-dyna file also has the same *node keyword
                index = f_content_line_list.index(line)
                next_ind = index + 1
                while next_ind <= len(f_content_line_list) and f_content_line_list[next_ind].startswith('$'):
                    next_ind += 1
                next_line = f_content_line_list[next_ind].strip()
                if re.match(r'^\d+', next_line) and not re.search(r',', next_line):
                    return True
            if line.startswith('*INCLUDE') or line.startswith('*include'):
                index = f_content_line_list.index(line)
                next_ind = index + 1
                while next_ind <= len(f_content_line_list) and f_content_line_list[next_ind].startswith('$'):
                    next_ind += 1
                next_line = f_content_line_list[next_ind].strip()
                include_fname = next_line
                include_fpath = os.path.join(os.path.dirname(fpath), include_fname)
                if os.path.isfile(include_fpath):
                    if is_lsdyna_file_by_content(include_fpath):
                        return True
    return False


if __name__ == "__main__":
    fpath = 'E:/Works/GitProject/fem_utils/tests/data/dyna(.k)/quad_no_ext'
    print(is_lsdyna_file(fpath))