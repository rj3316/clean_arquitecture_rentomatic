from os import remove

from .repo import Repo
from ..infraestructure.ControllerFileHandler import FileHandler
from ..domain.room import Room

class RepoFile(Repo):
    def _initialize(self, config = None):
        try: self.file = config['file']
        except: self.file = None

    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, value):
        self._file = value

    def write(self, data):
        FileHandler.write(self.file, data)

    def read(self, domain = None):
        ret_val, _ = FileHandler.read(self.file)

        if isinstance(domain, str): ret_val = ret_val[domain]
        try:
            ret_val = [Room.from_dict(i) for i in ret_val]
        except:
            ret_val = None

        return ret_val
    
    def initialize(self):
        FileHandler.delete(self.file)