import os


class AllFile(object):
    def __init__(self):
        self._all_files_dict = dict()
        self._master_files = dict()

    def find_master_file(self, path, multi_master_file=False):
        path_list = list()
        if isinstance(path, str):
            assert os.path.isdir(path)
            for root, dirs, files in os.walk(path):
                for path in files:
                    path_list.append(os.path.join(root, path))
        elif isinstance(path, list):
            for value in path:
                assert os.path.isfile(value)
            path_list = path
        else:
            raise ValueError

        for file_path in path_list:
            file_full_name = file_path.split('/')[-1].upper()
            file_ext = file_full_name.split('.')[-1].upper()
            self.all_files_dict[file_full_name] = FileInform(file_path, file_ext)

        for key in self.all_files_dict.keys():
            data = self.all_files_dict[key]
            if data.file_ext == 'INP':
                self.abaqus_file_process(data)
            elif data.file_ext in ('K', 'KEY'):
                self.lsdyna_file_process(data)
            elif data.file_ext in ('BDF', 'NAS'):
                self.nastran_file_process(data)
            elif data.file_ext == 'FEM':
                self.optistruct_file_process(data)
            elif data.file_ext in ('CDB', 'STL', 'OBJ', 'OFF', 'PLY'):
                pass
            else:
                self.all_files_dict.pop(key)

        for key in self.all_files_dict.keys():
            if not self.all_files_dict[key].master_file_path:
                self.master_files[key] = self.all_files_dict[key]

        if len(self.master_files) == 1:
            return self.master_files.values()[0].file_path
        elif len(self.master_files) > 1:
            if multi_master_file:
                return [self.master_files[key].file_path for key in self.master_files]
            else:
                return [self.master_files[key].file_path for key in self.master_files][0]
        else:
            return None

    def abaqus_file_process(self, data):
        with open(data.file_path, 'r') as fo:
            while 1:
                line = fo.readline()
                if not line:
                    break
                line.strip()
                fields = line.split(',')
                if fields[0].upper() == '*INCLUDE':
                    file_full_name = fields[-1].split('=')[-1].strip().upper()
                    slave_file = self.all_files_dict[file_full_name]
                    slave_file.master_file_path = data.file_path
                    data.slave_file_path = slave_file.file_path

    def lsdyna_file_process(self, data):
        line_process_switch = False
        with open(data.file_path, 'r') as fo:
            while 1:
                line = fo.readline()
                if not line:
                    break
                line = line.strip()
                if line.upper().startswith('*INCLUDE'):
                    line_process_switch = True
                elif line.upper().startswith('*'):
                    line_process_switch = False
                if line_process_switch and not line.startswith('*'):
                    file_full_name = line.split('/')[-1].strip().upper()
                    slave_file = self.all_files_dict[file_full_name]
                    slave_file.master_file_path = data.file_path
                    data.slave_file_path = slave_file.file_path

    def nastran_file_process(self, data):
        with open(data.file_path, 'r') as fo:
            while 1:
                line = fo.readline()
                if not line:
                    break
                line.strip()
                fields = line.split(' ')
                if fields[0].upper() == 'INCLUDE':
                    file_full_name = fields[-1].split('/')[-1].strip().upper()
                    slave_file = self.all_files_dict[file_full_name]
                    slave_file.master_file_path = data.file_path
                    data.slave_file_path = slave_file.file_path

    def optistruct_file_process(self, data):
        with open(data.file_path, 'r') as fo:
            while 1:
                line = fo.readline()
                if not line:
                    break
                line.strip()
                fields = line.split(' ')
                if fields[0].upper() == 'INCLUDE':
                    file_full_name = fields[-1].split('/')[-1].strip().upper()
                    slave_file = self.all_files_dict[file_full_name]
                    slave_file.master_file_path = data.file_path
                    data.slave_file_path = slave_file.file_path

    @property
    def all_files_dict(self):
        return self._all_files_dict

    @property
    def master_files(self):
        return self._master_files


class FileInform(object):
    def __init__(self, input_file_path=None, file_ext=None):
        self._file_path = input_file_path
        self._file_ext = file_ext
        self._master_file_path = list()
        self._slave_file_path = list()

    def fix_master_file_path(self):
        pass

    def fix_slave_file_path(self):
        pass

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def file_ext(self):
        return self._file_ext

    @file_ext.setter
    def file_ext(self, value):
        self._file_ext = value

    @property
    def master_file_path(self):
        return self._master_file_path

    @master_file_path.setter
    def master_file_path(self, value):
        self._master_file_path.append(value)

    @property
    def slave_file_path(self):
        return self._slave_file_path

    @slave_file_path.setter
    def slave_file_path(self, value):
        self._slave_file_path.append(value)
