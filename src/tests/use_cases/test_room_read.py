from unittest import mock

from ...use_cases.room_read_all import ReadAll
from ...requests.room_read_request import build_room_read_request
from ...simulators.factorysimulator import FactorySimulator

def test_room_read_all():
    domain = 'room'

    repo = mock.Mock()
    repo.read.return_value = FactorySimulator.create_domain_objects(domain)

    request = build_room_read_request()

    response = ReadAll.read_all(repo, request, domain)

    # Verifimos que la respuesta del request es True
    assert bool(response) == True

    # Verificamos que el repo devuelve el valor esperado
    assert response.value == FactorySimulator.create_domain_objects(domain)