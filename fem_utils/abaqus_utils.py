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


def is_abaqus_file_by_content(fpath):
    with open(fpath, 'r+') as fp:
        f_content_line_list = fp.readlines()
        for line in f_content_line_list:
            if line.startswith('*NODE') or line.startswith('*node'):
                # compare the following five lines, because ls-dyna file also has the same *node keyword
                index = f_content_line_list.index(line)
                next_ind = index + 1
                while next_ind <= len(f_content_line_list) and f_content_line_list[next_ind].startswith('**'):
                    next_ind += 1
                next_line = f_content_line_list[next_ind].strip()
                if re.match(r'^\d+', next_line) and re.search(r',', next_line):
                    return True
            if line.startswith('*INCLUDE') or line.startswith('*include'):
                line = line.strip()
                wordsInLine_list = line.split(',')
                if len(wordsInLine_list) > 1:
                    include_para = wordsInLine_list[1]
                    include_para = include_para.strip()
                    re_include_fname = re.match(r'''(.+?)=(.+)''', include_para)
                    if re_include_fname:
                        include_fname = re_include_fname.group(2)
                        include_fpath = os.path.join(os.path.dirname(fpath), include_fname)
                        if os.path.isfile(include_fpath):
                            if is_abaqus_file_by_content(include_fpath):
                                return True
    return False



if __name__ == "__main__":
    fpath = 'E:/Works/GitProject/fem_utils/tests/data/abaqus(.inp)/elements_no_ext'
    print(is_abaqus_file(fpath))
