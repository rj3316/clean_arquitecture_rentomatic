from abc import ABC, abstractmethod

class Repo(ABC):
    def __init__(self, *args, **kwargs):
        self._configuration(*args, **kwargs)
    
    def _configuration(self, *args, **kwargs):
        # Polymorphic method
        pass
    
    # INTERFACE PUBLIC METHODS
    def write(self, domain = None, data = None):
        return self._write(domain, data)

    def read(self, domain = None, filters = None):
        data = self._read(domain)

        if data is None: data = list()

        ret_val = self._apply_filters(data, filters)

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

    def _apply_filters(self, data, filters):
        # import pdb; pdb.set_trace()

        ret_val = data
        if isinstance(filters, dict) and filters != dict():
            ret_val = list()
            for filter, filter_value in filters.items():
                try:
                    filter_key = filter.split('__')[0]
                    filter_logic = filter.split('__')[1]

                    for tmp in data:
                        tmp_dict = tmp.to_dict()
                        if filter_key in tmp_dict.keys():
                            if filter_logic == 'eq':
                                cond = tmp_dict[filter_key] == filter_value
                            elif filter_logic == 'neq':
                                cond = tmp_dict[filter_key] != filter_value
                            elif filter_logic == 'lt':
                                cond = tmp_dict[filter_key] <= filter_value
                            elif filter_logic == 'lr':
                                cond = tmp_dict[filter_key] < filter_value
                            elif filter_logic == 'gt':
                                cond = tmp_dict[filter_key] >= filter_value
                            elif filter_logic == 'gr':
                                cond = tmp_dict[filter_key] > filter_value
                        
                            if cond: ret_val.append(tmp)
                except: pass
        
        return ret_val