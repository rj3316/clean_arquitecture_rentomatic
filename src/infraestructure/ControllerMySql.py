from ..legacy.MySql import MySql
from .controller import Controller

from ..domain.domainfactory import DomainFactory

class ControllerMySql(Controller):
    @classmethod
    def write(cls, ddbb_config, data = None):
        for key, value in data.items():
            if not cls._check_if_table_exists(ddbb_config, key): cls._create_domain_table(ddbb_config, key)

            if not isinstance(value, list): value = [value]

            config = cls._get_ddbb_config(ddbb_config)
            ddbb = MySql(config)
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

    @classmethod
    def _create_domain_table(cls, ddbb_config, domain):
        dom = DomainFactory.create(domain)
        fields = dom.describe()

        config = cls._get_ddbb_config(ddbb_config)
        ddbb = MySql(config)

        params = ddbb.get_param_manager()
        params.set_table(domain)

        for field in fields:
            params.set_columns(field[0])

            if field[1] == 'str':
                datatype = 'VARCHAR(100)'
            elif field[1] == 'int':
                datatype = 'INT'
            elif field[1] == 'float':
                datatype = 'FLOAT'
            elif field[1] == 'date':
                datatype = 'DATE'

            params.set_values(datatype)
        
        ddbb.create_table(params)

    @classmethod
    def _check_if_table_exists(cls, ddbb_config, domain):
        config = cls._get_ddbb_config(ddbb_config)
        ddbb = MySql(config)

        return ddbb.check_if_table_exists(domain)