import unittest
import os

from fem_utils import nastran_utils


class TestNastranUtils(unittest.TestCase):
    def setUp(self):
        self._model_dir = os.path.join(os.path.dirname(__file__), 'data', 'nastran(.bdf)')

    def get_model_path(self, fname):
        return os.path.join(self._model_dir, fname)

    def test_is_nastran_file_by_content(self):
        list_fileNname_isNastran = [
            ['elements.bdf', True],
            ["grids.bdf", True],
            ["nonsense.txt", False],
            ["quad.bdf", True],
            ['elements_no_ext', True],
            ['grids_no_ext', True],
            ['quad_no_ext', True]
        ]

        for file_name, is_nastran in list_fileNname_isNastran:
            self.assertEqual(
                nastran_utils.is_nastran_file(self.get_model_path(file_name)),
                is_nastran,
                msg='Check Error with file: %s' % file_name
            )

if __name__ == '__main__':
    unittest.main()
