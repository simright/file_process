import unittest
import os

from fem_utils import abaqus_utils


class TestAbaqusUtils(unittest.TestCase):
    def setUp(self):
        self._model_dir = os.path.join(os.path.dirname(__file__), 'data', 'abaqus(.inp)')

    def get_model_path(self, fname):
        return os.path.join(self._model_dir, fname)

    def test_is_abaqus_file_by_content(self):
        list_fileNname_isAbaqus = [
            ['elements.inp', True],
            ["nodes.inp", True],
            ["nonsense.txt", False],
            ["quad.inp", True],
            ["elements_no_ext", True],
            ["quad_no_ext", True]
        ]

        for file_name, is_abaqus in list_fileNname_isAbaqus:
            self.assertEqual(
                abaqus_utils.is_abaqus_file(self.get_model_path(file_name)),
                is_abaqus,
                msg='Check Error with file: %s' % file_name
            )

if __name__ == '__main__':
    unittest.main()
