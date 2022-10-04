import pytest

from ...factory.factory_request_builder import FactoryRequestBuilder

domain = 'room'

def test_room_build_read_request_without_parameters():
    # 
    request = FactoryRequestBuilder.create(domain).build_read_request()

    assert request.filters is None
    assert bool(request) is True

def test_room_build_read_requests_with_empty_filters():
    request = FactoryRequestBuilder.create(domain).build_read_request({})

    assert request.filters == {}
    assert bool(request) is True
        
def test_room_build_read_requests_with_invalid_filters_parameters():
    request = FactoryRequestBuilder.create(domain).build_read_request(filters=5)

    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False

def test_room_build_read_requests_with_incorrect_filter_keys():
    request = FactoryRequestBuilder.create(domain).build_read_request(filters={'a':1})
    
    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False

@pytest.mark.parametrize('key', ['price__lt', 'price__gt'])
def test_room_build_read_request_accepted_filters(key):
    filters = {key: 80}

    request = FactoryRequestBuilder.create(domain).build_read_request(filters = filters)

    assert request.filters == filters
    assert bool(request) is True

@pytest.mark.parametrize('key', ['code__lt', 'code__gt'])
def test_room_build_read_request_rejected_filters(key):
    filters = {key: 1}

    request = FactoryRequestBuilder.create(domain).build_read_request(filters = filters)

    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False

