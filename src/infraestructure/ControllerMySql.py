from ..legacy.MySql import MySql
from .controller import Controller

class ControllerMySql(Controller):
    @classmethod
    def write(cls, db_config, data = None):
        config = cls._get_db_config(db_config)
        db = MySql(config)

        for key, value in data.items():
            if not isinstance(value, list): value = [value]

            for d in value:
                params = db.get_param_manager()

                params.set_table(key)

                cols = list(d.keys())
                params.set_columns(cols)
                
                values = [i for _, i in d.items()]
                params.set_values(values)

                success = db.insert(params)

        cls.db = db

    @classmethod
    def read(cls, db_config, domain = None):
        ret_val = None

        if isinstance(domain, str):
            config = cls._get_db_config(db_config)
            db = MySql(config)

            params = db.get_param_manager()

            params.set_table(domain)
            ret_val = db.select(params)

        return ret_val

    @classmethod
    def initialize(cls, db_config, domain = None):
        ret_val = None

        if isinstance(domain, str):
            config = cls._get_db_config(db_config)
            db = MySql(config)

            params = db.get_param_manager()
            params.set_table(domain)
            ret_val = db.delete(params)
        
        return ret_val

    @classmethod
    def _get_db_config(cls, db_config):
        config = {
            'debug': True,
            'config': {}
            }

        config['config']['database'] = db_config
        return config
