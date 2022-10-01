from os import remove

from .repo import Repo
from ..infraestructure.ControllerFileHandler import FileHandler
from ..infraestructure.FormatterDict import FormatterDict
from ..domain.room import Room

class RepoFile(Repo):
    def _configuration(self, config = None):
        try: self.file = config['file']
        except: self.file = None

    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, value):
        self._file = value

    def _write(self, domain = None, data = None):
        # Leemos el valor actual
        current, _ = FileHandler.read(self.file)

        # Compactamos data con su dominio y concatenamos con el valor actual
        data = {domain: data}
        data = FormatterDict.concatenate_dictionaries(current, data)

        # Escribimos el nuevo valor
        FileHandler.write(self.file, data)

    def _read(self, domain = None):
        ret_val, _ = FileHandler.read(self.file)

        try:
            if isinstance(domain, str): ret_val = ret_val[domain]
            ret_val = [Room.from_dict(i) for i in ret_val]
        except:
            ret_val = None

        return ret_val
    
    def _initialize(self, domain):
        FileHandler.delete(self.file, domain)