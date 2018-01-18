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


def lsdyna_keywords_pattern():
    keywords_pattern = r'^(\*node_)|(\*element_)|(\*mat_)|(\*boundary_)|(\*include_)|(\*define_)|(\*contact_)|(\*set_)'
    return keywords_pattern


def is_lsdyna_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            line_lower = line.strip().lower()
            # if have *keyword, it must be lsdyna file
            if re.search(r'\*keyword', line_lower):
                return True
            # lsdyna and abaqus have the same keywords, *node/*element,
            # so if have this two keywords, must using the following content below the keywords to check
            # if have commas ",", must be abaqus file, otherwise, is lsdyna file
            if re.search(r'^(\*node)|(\*element)', line_lower):
                if re.search(r',', line_lower):
                    return False
                index = f_content_line_list.index(line)
                next_ind = index + 1
                if next_ind >= len(f_content_line_list):
                    return False
                while f_content_line_list[next_ind].strip().startswith('$'):
                    next_ind += 1
                next_line = f_content_line_list[next_ind].strip()
                if re.match(r'^\d+', next_line) and not re.search(r',', next_line):
                    return True
                return False
            if re.search(lsdyna_keywords_pattern(), line_lower):
                return True
            if line_lower == '*include':
                return True
        return False


if __name__ == "__main__":
    fpath = 'D:/worksCode/fem_utils/tests/data/dyna(.k)/nodes_no_ext'
    print(is_lsdyna_file(fpath))