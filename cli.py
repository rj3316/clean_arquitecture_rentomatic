from src.repository.repo_factory import RepoFactory
from src.use_cases.read_all import read_all

from src.simulators.domain.simulator_room import room_dicts
from src.simulators.infraestructure.simulator_file import file
from src.simulators.infraestructure.simulator_mysql import mysql

import pdb

testing = False
domain = 'room'

# Repo selector:
#   0. RAM
#   1. File
#   2. SQL
repo_selector = 1

if repo_selector == 0:
    repo_detail = 'RepoMem'
    config = None
elif repo_selector == 1:
    repo_detail = 'RepoFile'
    config = {'file': file}
elif repo_selector == 2:
    repo_detail = 'RepoSql'
    config = {'ddbb_config': mysql}

repo = RepoFactory.create(repo_detail, config)

result = read_all(repo, domain)

# Insertamos entidades de prueba
sim_rooms = room_dicts()
repo.write(domain = domain, data = sim_rooms)

result = read_all(repo, domain)







if testing: repo.initialize(domain)
