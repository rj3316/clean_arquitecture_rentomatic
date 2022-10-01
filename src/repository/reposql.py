from .repo import Repo
from ..infraestructure.ControllerMySql import ControllerMySql
from ..adapters.AdapterMySql import AdapterMySql
from ..domain.room import Room

class RepoSql(Repo):
    def _configuration(self, config = None):
        try: self.ddbb_config = config['ddbb_config']
        except: self.ddbb_config = None

    @property
    def ddbb_config(self):
        return self._ddbb_config

    @ddbb_config.setter
    def ddbb_config(self, value):
        self._ddbb_config = value

    def _write(self, domain = None, data = None):
        data = {domain: data}
        ControllerMySql.write(self.ddbb_config, data)

    def _read(self, domain = None):
        ret_val = None

        if isinstance(domain, str): #########!!!!!
            data = ControllerMySql.read(self.ddbb_config, domain)
            data = AdapterMySql.adapt_domain_from_sql(data)

            ret_val = [Room.from_dict(i) for i in data]
        
        return ret_val
    
    def _initialize(self, domain = None):
        ddbb_config = self.ddbb_config
        ret_val = ControllerMySql.initialize(ddbb_config, domain)
        return ret_val

