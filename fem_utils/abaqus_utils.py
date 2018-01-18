import os, re

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


def is_abaqus_file(fpath):
    if is_abaqus_fname(fpath):
        return True
    return is_abaqus_file_by_content(fpath)


def abaqus_keywords_pattern():
    keywords_pattern = r'^(\*node)|(\*element)|(\*material)|(\*part)|(\*boundary)|(\*step)|(\*include)|(\*cloud)|(\*dload)'
    return keywords_pattern


def is_abaqus_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            line_lower = line.strip().lower()
            if re.search(r'\*heading', line_lower):
                return True
            if re.search(abaqus_keywords_pattern(), line_lower):
                if re.search(r',', line_lower):
                    return True
                # compare the following lines, because ls-dyna file also has the same *node keyword
                index = f_content_line_list.index(line)
                next_ind = index + 1
                if next_ind >= len(f_content_line_list):
                    return False
                while f_content_line_list[next_ind].startswith('**'):
                    next_ind += 1
                next_line = f_content_line_list[next_ind].strip()
                if re.match(r'^\d+', next_line) and re.search(r',', next_line):
                    return True
        return False


if __name__ == "__main__":
    fpath = 'D:/worksCode/fem_utils/tests/data/abaqus(.inp)/elements_no_ext'
    print(is_abaqus_file(fpath))
