from .repo import Repo

from ..domain.room import Room

class RepoMem(Repo):
    def _initialize(self, config = None):
        try: self.data = config['data']
        except: self.data = None

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value
            
    def write(self, data):
        self.data = data

    def read(self, domain = None):
        ret_val = None
        if domain is not None:
            data = self.data[domain]
            ret_val = [Room.from_dict(i) for i in data]
        
        return ret_val
    
    def initialize(self):
        self.data = None