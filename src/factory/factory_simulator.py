from ..simulators.domain.simulator_room import room_dicts, rooms
from ..simulators.domain.simulator_hotel import hotel_dicts, hotels
from ..simulators.domain.simulator_converter import converter_dicts, converters

from ..simulators.infraestructure.simulator_file import file
from ..simulators.infraestructure.simulator_mysql import mysql

class FactorySimulator:
    @classmethod
    def create_domain_dicts(cls, domain = None, filters = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                tmps = room_dicts()
            elif domain == 'hotel':
                tmps = hotel_dicts()
            elif domain == 'converter':
                tmps = converter_dicts()
        
        ret_val = list()
        if filters is not None:
            for filter, filter_value in filters.items():
                try:
                    filter_key = filter.split('__')[0]
                    filter_logic = filter.split('__')[1]

                    for tmp in tmps:
                        if filter_key in tmp.keys():
                            if filter_logic == 'eq':
                                cond = tmp[filter_key] == filter_value
                            elif filter_logic == 'neq':
                                cond = tmp[filter_key] != filter_value
                            elif filter_logic == 'lt':
                                cond = tmp[filter_key] <= filter_value
                            elif filter_logic == 'lr':
                                cond = tmp[filter_key] < filter_value
                            elif filter_logic == 'gt':
                                cond = tmp[filter_key] >= filter_value
                            elif filter_logic == 'gr':
                                cond = tmp[filter_key] > filter_value
                        
                            if cond: ret_val.append(tmp)
                except: pass
        else:
            ret_val = tmps

        return ret_val
    
    @classmethod
    def create_domain_objects(cls, domain = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                ret_val = rooms()
            elif domain == 'hotel':
                ret_val = hotels()
            elif domain == 'converter':
                ret_val = converters()
        
        return ret_val

    @classmethod
    def create_repository_config(cls, repo_type = None):
        ret_val = None

        if repo_type == 'RepoFile':
            ret_val = {'file': file}
        elif repo_type == 'RepoSql':
            ret_val = {'ddbb_config': mysql}
        
        return ret_val