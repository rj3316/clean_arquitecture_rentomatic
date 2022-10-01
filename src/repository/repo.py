from abc import ABC, abstractmethod

class Repo(ABC):
    def __init__(self, *args, **kwargs):
        self._configuration(*args, **kwargs)
    
    def _configuration(self, *args, **kwargs):
        # Polymorphic method
        pass
    
    def write(self, domain = None, data = None):
        return self._write(domain, data)

    def read(self, domain = None, verbose = False):
        ret_val = self._read(domain)
        if ret_val is None: ret_val = list()

        if verbose: print(ret_val)

        return ret_val

    def initialize(self, domain = None):
        return self._initialize(domain)

    @abstractmethod
    def _write(self):
        pass

    @abstractmethod
    def _read(self):
        pass

    @abstractmethod
    def _initialize(self):
        pass