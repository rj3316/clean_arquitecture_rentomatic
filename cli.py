from src.repository.repo_factory import RepoFactory
from src.use_cases.read import Read

from src.domain.domainfactory import DomainFactory
from src.requests.builder_read_request import BuilderReadRequest
from src.simulators.factorysimulator import FactorySimulator

# from src.simulators.domain.simulator_room import room_dicts
# from src.simulators.domain.simulator_hotel import hotel_dicts
# from src.simulators.infraestructure.simulator_file import file
# from src.simulators.infraestructure.simulator_mysql import mysql

testing = True

# Domain selector:
#   0. Room
#   1. Hotel
domain_selector = 0

if domain_selector == 0:
    domain = 'room'

elif domain_selector == 1:
    domain = 'hotel'

sims = FactorySimulator.create_domain_dicts(domain)
domains = DomainFactory.create(domain, sims)

# Repo selector:
#   0. RAM
#   1. File
#   2. SQL
repo_selector = 2

if repo_selector == 0:
    repo_detail = 'RepoMem'
elif repo_selector == 1:
    repo_detail = 'RepoFile'
elif repo_selector == 2:
    repo_detail = 'RepoSql'

# Filter selector:
#   0. No filter
#   1. filter_price__gt: 50
#   2. filter_size__lt: 150
filter_selector = 2
if filter_selector == 0:
    filters = None
elif filter_selector == 1:
    filters = {'filter_price__gt': 50}
elif filter_selector == 2:
    filters = {'filter_size__lt': 150}

config = FactorySimulator.create_repository_config(repo_detail)
repo   = RepoFactory.create(repo_detail, config)

# Contruimos la request
query_request = {
    'filters': {}
}

if filters is not None:
    for arg, value in filters.items():
        if arg.startswith('filter_'): query_request['filters'][arg.replace('filter_', '')] = value

req = BuilderReadRequest.build_read_request(query_request['filters'])

result = Read.read(repo, req, domain)
print(result.value)

# Insertamos entidades de prueba
repo.write(domain = domain, data = sims)

result = Read.read(repo, req, domain)
print(result.value)

if testing: repo.initialize(domain)
