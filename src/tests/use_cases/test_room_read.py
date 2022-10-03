from unittest import mock

from ...responses import ResponseTypes

from ...use_cases.room_read import RoomRead
from ...requests.room_read_request import BuilderRoomReadRequest
from ...simulators.factorysimulator import FactorySimulator

domain = 'room'

def test_room_read_without_parameters():
    repo = mock.Mock()
    repo.read.return_value = FactorySimulator.create_domain_objects(domain)

    request = BuilderRoomReadRequest.build_room_read_request()

    response = RoomRead.read(repo, request, domain)

    # Verifimos que la respuesta del request es True
    assert bool(response) == True

    # Verificamos que el repo devuelve el valor esperado
    assert response.value == FactorySimulator.create_domain_objects(domain)

def test_room_read_with_filters():
    repo = mock.Mock()
    repo.read.return_value = FactorySimulator.create_domain_objects(domain)

    query_filters = {'code__eq': 5}
    request = BuilderRoomReadRequest.build_room_read_request(filters = query_filters)

    response = RoomRead.read(repo, request, domain)

    assert bool(response) is True
    assert response.value == FactorySimulator.create_domain_objects(domain)

def test_room_read_handles_generic_error():
    repo = mock.Mock()
    repo.read.side_effect = Exception("Just an error message")

    query_filters = {}
    request = BuilderRoomReadRequest.build_room_read_request(filters = query_filters)

    response = RoomRead.read(repo, request, domain)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': "Exception: Just an error message"
    }

def test_room_read_handles_bad_request():
    repo = mock.Mock()

    query_filters = 5
    request = BuilderRoomReadRequest.build_room_read_request(filters = query_filters)

    response = RoomRead.read(repo, request, domain)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': "filters: Is not iterable"
    }