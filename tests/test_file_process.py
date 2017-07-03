import unittest
import os
import shutil
import filecmp

from file_process.master_file import AllFile


class TestFileProcess(unittest.TestCase):
    def setUp(self):
        self.fullpath_dir_of_models = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data'))

    def get_model_path(self, fname):
        return os.path.join(self.fullpath_dir_of_models, fname)

    def test_io(self, overwrite=False):
        print 'Testing File Process ...'

        fname = [
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
        list_file_path = list()

        for filename in fname:
            list_file_path.append(self.get_model_path(filename))

        all_file = AllFile()
        master_file_path = all_file.find_master_file(list_file_path)

        fpath_out_ref = self.get_model_path('master_file_path.ref')
        fpath_out_new = fpath_out_ref[:-4] + '.new'
        fo = open(fpath_out_new, 'w')
        for line in master_file_path:
            fo.write(line + '\n')
        fo.close()

        self.assertTrue(os.path.isfile(fpath_out_new))
        if not os.path.isfile(fpath_out_ref):
            print 'WARNING: REF file not exist!'
            shutil.copyfile(fpath_out_new, fpath_out_ref)
            print '  COPYing: %s' % fpath_out_new
            print '  To     : %s' % fpath_out_ref

        if filecmp.cmp(fpath_out_ref, fpath_out_new, shallow=False):
            os.remove(fpath_out_new)
        else:
            if overwrite:
                shutil.move(fpath_out_new, fpath_out_ref)
            else:
                self.fail('Diffs found in:\n' + '  ' + fpath_out_ref + '\n' + '  ' + fpath_out_new)

if __name__ =='__main__':
    unittest.main()