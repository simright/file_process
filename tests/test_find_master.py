import unittest
import os

from fem_utils.master_file import find_master


class TestFindMaster(unittest.TestCase):

    def test_io(self):
        print 'Testing File Process ...'

        list_folder_name = [
                    "data/abaqus(.inp)",
                    "data/nastran(.bdf)",
                    "data/optistruct(.fem)",
                    "data/dyna(.k)",
                    "data/ansys(.cdb)",
        ]

        all_master_file_path = [
                    "data/optistruct(.fem)/quad.fem",
                    "data/nastran(.bdf)/quad.bdf",
                    "data/dyna(.k)/quad.k",
                    "data/abaqus(.inp)/quad.inp",
                    "data/ansys(.cdb)/cloads.cdb"
        ]

        # paths of all files are given
        for test_folder_name in list_folder_name:
            all_file_path = list()
            for root, dirs, files in os.walk(test_folder_name):
                for path in files:
                    all_file_path.append(os.path.join(root, path))

            master_file_path = find_master(all_file_path)

            if type(master_file_path) == str:
                assert master_file_path in all_master_file_path
            elif type(master_file_path) == list:
                for path in master_file_path:
                    assert path in all_master_file_path
            else:
                raise ValueError

        # path of folder is given
        for test_folder_name in list_folder_name:
            master_file_path = find_master(test_folder_name)

            if type(master_file_path) == str:
                assert master_file_path in all_master_file_path
            elif type(master_file_path) == list:
                for path in master_file_path:
                    assert path in all_master_file_path
            else:
                raise ValueError

        print 'Test passed'

if __name__ == '__main__':
    unittest.main()
