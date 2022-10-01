from ..legacy.MySql import MySql
from .controller import Controller

class ControllerMySql(Controller):
    @classmethod
    def write(cls, ddbb_config, data = None):
        config = cls._get_ddbb_config(ddbb_config)
        ddbb = MySql(config)

        for key, value in data.items():
            if not isinstance(value, list): value = [value]

            for d in value:
                params = ddbb.get_param_manager()

                params.set_table(key)

                cols = list(d.keys())
                params.set_columns(cols)
                
                values = [i for _, i in d.items()]
                params.set_values(values)

                success = ddbb.insert(params)

        cls.ddbb = ddbb

    @classmethod
    def read(cls, ddbb_config, domain = None):
        ret_val = None

        if isinstance(domain, str):
            config = cls._get_ddbb_config(ddbb_config)
            ddbb = MySql(config)

            params = ddbb.get_param_manager()

            params.set_table(domain)
            ret_val = ddbb.select(params)

        return ret_val

    @classmethod
    def initialize(cls, ddbb_config, domain = None):
        ret_val = None

        if isinstance(domain, str):
            config = cls._get_ddbb_config(ddbb_config)
            ddbb = MySql(config)

            params = ddbb.get_param_manager()
            params.set_table(domain)
            ret_val = ddbb.delete(params)
        
        return ret_val

    @classmethod
    def _get_ddbb_config(cls, ddbb_config):
        config = {
            'debug': True,
            'config': {}
            }

        config['config']['database'] = ddbb_config
        return config
