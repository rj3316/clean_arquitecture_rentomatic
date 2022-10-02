from .domain.simulator_room import room_dicts, rooms
from .domain.simulator_hotel import hotel_dicts, hotels

from .infraestructure.simulator_file import file
from .infraestructure.simulator_mysql import mysql

class FactorySimulator:
    @classmethod
    def create_domain_dicts(cls, domain = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                ret_val = room_dicts()
            elif domain == 'hotel':
                ret_val = hotel_dicts()
        
        return ret_val
    
    @classmethod
    def create_domain_objects(cls, domain = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                ret_val = rooms()
            elif domain == 'hotel':
                ret_val = hotels()
        
        return ret_val


    @classmethod
    def create_repository_config(cls, repo_type = None):
        ret_val = None

        if repo_type == 'RepoFile':
            ret_val = {'file': file}
        elif repo_type == 'RepoSql':
            ret_val = {'ddbb_config': mysql}
        
        return ret_val