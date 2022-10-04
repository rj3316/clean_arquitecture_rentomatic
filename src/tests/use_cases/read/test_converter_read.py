from unittest import mock

from ....responses import ResponseTypes

from ....use_cases.converter_read import ConverterRead
from ....requests.builder_converter_read_request import BuilderConverterReadRequest
from ....factory.factory_simulator import FactorySimulator

domain = 'converter'

def test_converter_read_without_parameters():
    repo = mock.Mock()
    repo.read.return_value = FactorySimulator.create_domain_objects(domain)

    request = BuilderConverterReadRequest.build_read_request()

    response = ConverterRead.read(repo, request, domain)

    # Verifimos que la respuesta del request es True
    assert bool(response) == True

    # Verificamos que el repo devuelve el valor esperado
    assert response.value == FactorySimulator.create_domain_objects(domain)

def test_converter_read_with_filters():
    repo = mock.Mock()
    repo.read.return_value = FactorySimulator.create_domain_objects(domain)

    query_filters = {'code__eq': 5}
    request = BuilderConverterReadRequest.build_read_request(filters = query_filters)

    response = ConverterRead.read(repo, request, domain)

    assert bool(response) is True
    assert response.value == FactorySimulator.create_domain_objects(domain)

def test_converter_read_handles_generic_error():
    repo = mock.Mock()
    repo.read.side_effect = Exception("Just an error message")

    query_filters = {}
    request = BuilderConverterReadRequest.build_read_request(filters = query_filters)

    response = ConverterRead.read(repo, request, domain)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': "Exception: Just an error message"
    }

def test_converter_read_handles_bad_request():
    repo = mock.Mock()

    query_filters = 5
    request = BuilderConverterReadRequest.build_read_request(filters = query_filters)

    response = ConverterRead.read(repo, request, domain)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': "filters: Is not iterable"
    }