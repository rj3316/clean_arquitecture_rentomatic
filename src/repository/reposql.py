from .repo import Repo
from ..infraestructure.ControllerMySql import ControllerMySql

from ..domain.room import Room

class RepoSql(Repo):
    def _initialize(self, config = None):
        try: self.db = config['db']
        except: self.db = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    def write(self, data):
        ControllerMySql.write(self.db, data)

    def read(self, domain = None):
        ret_val = None

        if domain is not None:
            data = ControllerMySql.read(self.db, domain)
            data = self._adapt_domains(data)

            ret_val = [Room.from_dict(i) for i in data]
        
        return ret_val
    
    def initialize(self, domain = None):
        db_config = self.db
        ControllerMySql.initialize(db_config, domain)

    def _adapt_domains(self, data):
        ret_val = list()

        for code, size, price, longitude, latitude in zip(data['code'], data['size'], data['price'], data['longitude'], data['latitude']):
            domain = {
                'code': code,
                'size': size,
                'price': price,
                'longitude': longitude,
                'latitude': latitude,
            }
            ret_val.append(domain)

        return ret_val