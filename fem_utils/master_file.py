import os

from fem_utils import abaqus_utils
from fem_utils import ansys_utils
from fem_utils import lsdyna_utils
from fem_utils import nastran_utils
from fem_utils import optistruct_utils


def find_includes_by_files(files):
    result = list()
    for fpath in files:
        assert os.path.isfile(fpath)
        if abaqus_utils.is_abaqus_fname(fpath):
            result.extend(abaqus_utils.get_include_files(fpath))
        elif ansys_utils.is_ansys_fname(fpath):
            result.extend(ansys_utils.get_include_files(fpath))
        elif lsdyna_utils.is_lsdyna_fname(fpath):
            result.extend(lsdyna_utils.get_include_files(fpath))
        elif nastran_utils.is_nastran_fname(fpath):
            result.extend(nastran_utils.get_include_files(fpath))
        elif optistruct_utils.is_optistruct_fname(fpath):
            result.extend(optistruct_utils.get_include_files(fpath))

    return result


def is_fem_fname(fpath):
    return abaqus_utils.is_abaqus_fname(fpath) or \
           ansys_utils.is_ansys_fname(fpath) or \
           lsdyna_utils.is_lsdyna_fname(fpath) or \
           ansys_utils.is_ansys_fname(fpath) or \
           nastran_utils.is_nastran_fname(fpath) or \
           optistruct_utils.is_optistruct_fname(fpath)


def find_master(path):
    if isinstance(path, str):
        return find_master_by_folder(path)
    elif isinstance(path, list):
        return find_master_by_files(path)
    else:
        raise ValueError


def find_masters_by_files(files):
    include_files = find_includes_by_files(files)
    master_files = list()
    for fpath in files:
        assert os.path.isfile(fpath)
        if is_fem_fname(fpath):
            if fpath not in include_files:
                master_files.append(fpath)

    return master_files


def find_masters_by_folder(folder):
    assert os.path.isdir(folder)

    list_files = list()
    for root, dirs, files in os.walk(folder):
        for path in files:
            list_files.append(os.path.join(root, path))

    return find_masters_by_files(list_files)


def find_master_by_files(files):
    master_files = find_masters_by_files(files)
    if len(master_files) > 0:
        assert len(master_files) == 1
        return master_files[0]

    return None


def find_master_by_folder(folder):
    master_files = find_masters_by_folder(folder)
    if len(master_files) > 0:
        assert len(master_files) == 1
        return master_files[0]

    return None
