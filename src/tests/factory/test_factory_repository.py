import pytest

from ...factory.factory_domain import FactoryDomain
from ...factory.factory_simulator import FactorySimulator
from ...domain.converter import Converter

domain = 'converter'
init_dicts = FactorySimulator.create_domain_dicts(domain)

@pytest.mark.factory
def test_create_converter_domain_entity():
    reals = FactoryDomain.create(domain, init_dicts)

    expected = [Converter.from_dict(dom) for dom in init_dicts]

    assert reals == expected