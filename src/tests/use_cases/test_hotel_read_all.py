from unittest import mock

from ...use_cases.read_all import ReadAll
from ...simulators.factorysimulator import FactorySimulator

def test_hotel_read_all():
    domain = 'hotel'

    repo = mock.Mock()
    repo.read.return_value = FactorySimulator.create_domain_objects(domain)

    result = ReadAll.read_all(repo, domain)

    # Verificamos que el repo devuelve el valor esperado
    assert result == FactorySimulator.create_domain_objects(domain)