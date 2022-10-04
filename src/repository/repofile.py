from .repo import Repo
from ..factory.factory_domain import FactoryDomain
from ..infraestructure.ControllerFileHandler import FileHandler
from ..infraestructure.FormatterDict import FormatterDict

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
        current = FileHandler.read(self.file)

        # Compactamos data con su dominio y concatenamos con el valor actual
        data = {domain: data}
        data = FormatterDict.concatenate_dictionaries(current, data)

        # Escribimos el nuevo valor
        FileHandler.write(self.file, data)

    def _read(self, domain = None):
        ret_val = list()

        try:
            domains = FileHandler.read(self.file)
            if domain in domains:
                ret_val = FactoryDomain.create(domain, domains[domain])
        except Exception as e:
            pass

        return ret_val
    
    def _initialize(self, domain):
        data = FileHandler.read(self.file)

        try:
            if domain in data.keys():
                data[domain] = list()
                FileHandler.write(self.file, data)
        except: pass
        