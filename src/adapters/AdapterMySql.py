    
from dataclasses import dataclass
from copy import deepcopy

class AdapterMySql:
    @classmethod
    def adapt_domain_from_sql(self, data):
        ret_val = list()

        try: fields = list(data.keys())
        except: fields = list()

        try: n = len(data[fields[0]])
        except: n = 0

        domains = list()
        for i in range(n):
            domain = {}
            for field in fields:
                domain[field] = None
            domains.append(domain)

        for field in fields:
            values = data[field]
            for i, value in enumerate(values):
                domains[i][field]  = deepcopy(value)
            
        return domains