from .repo import Repo

from ..domain.room import Room

class RepoMem(Repo):
    def _configuration(self, config = None):
        self.data = {}

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value
            
    def _write(self, domain = None, data = None):
        self.data[domain] = data

    def _read(self, domain = None):
        ret_val = None
        if domain in self.data.keys():ret_val = [Room.from_dict(i) for i in self.data[domain]]
        
        return ret_val
    
    def _initialize(self, domain):
        if domain in self.data.keys(): self.data[domain] = list()