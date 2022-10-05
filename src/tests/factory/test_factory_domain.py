import pytest

from ...factory.factory_domain import FactoryDomain
from ...factory.factory_simulator import FactorySimulator

from ...domain.converter import Converter
from ...domain.room import Room
from ...domain.hotel import Hotel

@pytest.mark.factory
def test_create_converter_domain_entity_from_dicts():
    domain = 'converter'
    doms = FactorySimulator.create_domain_dicts(domain)

    reals = FactoryDomain.create(domain, doms)

    expected = [Converter.from_dict(dom) for dom in doms]

    assert reals == expected

@pytest.mark.factory
def test_create_converter_domain_entity_from_none():
    domain = 'converter'

    reals = FactoryDomain.create(domain, None)

    expected = Converter()

    assert reals == expected

@pytest.mark.factory
def test_create_converter_domain_entity_invalid():
    domain = 'converter'

    reals = FactoryDomain.create(domain, 5)

    assert reals == None


@pytest.mark.factory
def test_create_room_domain_entity_from_dicts():
    domain = 'room'
    doms = FactorySimulator.create_domain_dicts(domain)

    reals = FactoryDomain.create(domain, doms)

    expected = [Room.from_dict(dom) for dom in doms]

    assert reals == expected

@pytest.mark.factory
def test_create_room_domain_entity_from_none():
    domain = 'room'

    reals = FactoryDomain.create(domain, None)

    expected = Room()

    assert reals == expected

@pytest.mark.factory
def test_create_room_domain_entity_invalid():
    domain = 'room'

    reals = FactoryDomain.create(domain, 5)

    assert reals == None

@pytest.mark.factory
def test_create_hotel_domain_entity_from_dicts():
    domain = 'hotel'
    doms = FactorySimulator.create_domain_dicts(domain)

    reals = FactoryDomain.create(domain, doms)

    expected = [Hotel.from_dict(dom) for dom in doms]

    assert reals == expected


@pytest.mark.factory
def test_create_hotel_domain_entity_from_none():
    domain = 'hotel'

    reals = FactoryDomain.create(domain, None)

    expected = Hotel()

    assert reals == expected

@pytest.mark.factory
def test_create_hotel_domain_entity_invalid():
    domain = 'hotel'

    reals = FactoryDomain.create(domain, 5)

    assert reals == None    