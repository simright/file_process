import unittest
import os

from fem_utils.master_file import find_master


class TestFindMaster(unittest.TestCase):
    def setUp(self):
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_io(self):
        list_folder_master = [
            ["abaqus(.inp)",     "quad.inp"],
            ["nastran(.bdf)",    "quad.bdf"],
            ["optistruct(.fem)", "quad.fem"],
            ["dyna(.k)",         "quad.k"],
            ["ansys(.cdb)",      "cloads.cdb"],
            #["nastran2",         "A320.bdf"]
        ]

        for test_folder_name, master_name in list_folder_master:
            test_folder_path = os.path.join(self._data_dir, test_folder_name)

            # paths of all files are given
            all_file_path = list()
            for root, dirs, files in os.walk(test_folder_path):
                for path in files:
                    all_file_path.append(os.path.join(root, path))

            master_file_path = find_master(all_file_path)

            if isinstance(master_file_path, str):
                self.assertEqual(os.path.normpath(master_file_path), os.path.normpath(os.path.join(test_folder_path, master_name)))
            elif isinstance(master_file_path, list):
                self.assertIn(os.path.normpath(os.path.join(test_folder_path, master_name)), master_file_path)
            else:
                raise ValueError

            # path of folder is given
            master_file_path = find_master(test_folder_path)
            if type(master_file_path) == str:
                self.assertEqual(os.path.normpath(master_file_path), os.path.normpath(os.path.join(test_folder_path, master_name)))
            elif type(master_file_path) == list:
                self.assertIn(os.path.normpath(os.path.join(test_folder_path, master_name)), master_file_path)
            else:
                raise ValueError


if __name__ == '__main__':
    unittest.main()
