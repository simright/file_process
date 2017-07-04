import unittest
import os

from file_process.master_file import AllFile


class TestFileProcess(unittest.TestCase):
    def setUp(self):
        self.fullpath_dir_of_models = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data'))

    def get_model_path(self, fname):
        return os.path.join(self.fullpath_dir_of_models, fname)

    def test_io(self):
        print 'Testing File Process ...'

        all_fname = [
                    "includes/nodes.k",
                    "includes/elements.k",
                    "elements.fem",
                    "elements.inp",
                    "quad.fem",
                    "quad.bdf",
                    "grids.bdf",
                    "nodes.inp",
                    "elements.bdf",
                    "quad.k",
                    "grids.fem",
                    "quad.inp",
                    ]
        master_fname = [
                    "quad.fem",
                    "quad.bdf",
                    "quad.k",
                    "quad.inp",
                       ]
        list_all_file_path = list()
        list_master_file_path = list()

        for filename in master_fname:
            list_master_file_path.append(self.get_model_path(filename))
        for filename in all_fname:
            list_all_file_path.append(self.get_model_path(filename))

        all_file = AllFile()
        found_master_file_path = all_file.find_master_file(list_all_file_path)

        for path in found_master_file_path:
            assert path in list_master_file_path
        assert len(found_master_file_path) == len(master_fname)
        print 'Test passed'

if __name__ == '__main__':
    unittest.main()
