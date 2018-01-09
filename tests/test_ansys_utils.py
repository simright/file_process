import unittest
import os

from fem_utils import ansys_utils


class TestAnsysUtils(unittest.TestCase):
    def setUp(self):
        self._model_dir = os.path.join(os.path.dirname(__file__), 'data', 'ansys(.cdb)')

    def get_model_path(self, fname):
        return os.path.join(self._model_dir, fname)

    def test_is_ansys_file_by_content(self):
        list_fileNname_isAnsys = [
            ['cloads.cdb', True],
            ["cloads_no_ext", True],
            ["nonsense.txt", False]
        ]

        for file_name, is_ansys in list_fileNname_isAnsys:
            self.assertEqual(
                ansys_utils.is_ansys_file(self.get_model_path(file_name)),
                is_ansys,
                msg='Check Error with file: %s' % file_name
            )

if __name__ == '__main__':
    unittest.main()
