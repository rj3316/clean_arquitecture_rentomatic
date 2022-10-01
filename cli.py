from src.repository.repo_factory import RepoFactory
from src.use_cases.read_all import read_all

from src.simulators.domain.simulator_room import room_dicts
from src.simulators.infraestructure.simulator_file import file
from src.simulators.infraestructure.simulator_mysql import mysql

import pdb

testing = False
domain = 'room'

# repo_detail = 'mem'

# repo_detail = 'file'
repo_detail = 'sql'

if repo_detail == 'mem':
    repo_detail = 'RepoMem'
    config = None
elif repo_detail == 'file':
    repo_detail = 'RepoFile'
    config = {'file': file}
elif repo_detail == 'sql':
    repo_detail = 'RepoSql'
    config = {'ddbb_config': mysql}

repo = RepoFactory.create(repo_detail, config)

result = read_all(repo, domain)

# Insertamos entidades de prueba
sim_rooms = room_dicts()
repo.write(domain = domain, data = sim_rooms)

result = read_all(repo, domain)







if testing: repo.initialize(domain)
