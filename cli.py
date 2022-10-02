from src.repository.repo_factory import RepoFactory
from src.use_cases.read_all import ReadAll

from src.domain.domainfactory import DomainFactory
from src.simulators.domain.simulator_room import room_dicts
from src.simulators.domain.simulator_hotel import hotel_dicts
from src.simulators.infraestructure.simulator_file import file
from src.simulators.infraestructure.simulator_mysql import mysql

testing = False

# Domain selector:
#   0. Room
#   1. Hotel
domain_selector = 1

if domain_selector == 0:
    domain = 'room'
    sims = room_dicts()

elif domain_selector == 1:
    domain = 'hotel'
    sims = hotel_dicts()

domains = DomainFactory.from_dicts(domain, sims)

# Repo selector:
#   0. RAM
#   1. File
#   2. SQL
repo_selector = 2

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

result = ReadAll.read_all(repo, domain, verbose=True)

# Insertamos entidades de prueba
repo.write(domain = domain, data = sims)

result = ReadAll.read_all(repo, domain, verbose=True)

if testing: repo.initialize(domain)
