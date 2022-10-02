from .repo import Repo
from ..domain.domainfactory import DomainFactory

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
        ret_val = list()

        try:
            domains = self.data
            if domain in domains.keys(): ret_val = DomainFactory.from_dicts(domain, self.data[domain])
        except: pass
                
        return ret_val
    
    def _initialize(self, domain):
        if domain in self.data.keys(): self.data[domain] = list()