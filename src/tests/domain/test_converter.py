import uuid
import json

from ...domain.converter import Converter
from ...domain.domainfactory import DomainFactory
from ...serializers.factoryserializer import SerializerFactory
from ...simulators.factorysimulator import FactorySimulator

domain = 'converter'

init_dict = FactorySimulator.create_domain_dicts(domain)[0]
init_dict['code'] = uuid.uuid4()
def test_converter_model_init():
    dom = Converter(
        code = init_dict['code'],
        serial = init_dict['serial'],
        host = init_dict['host'],
        rated = init_dict['rated'],
        power = init_dict['power'],
        soc = init_dict['soc'],
    )

    assert dom.code == init_dict['code']
    assert dom.serial == init_dict['serial']
    assert dom.host == init_dict['host']
    assert dom.rated == init_dict['rated']
    assert dom.power == init_dict['power']
    assert dom.soc == init_dict['soc']

def test_converter_model_from_dict():
    dom = DomainFactory.create(domain, init_dict)

    assert dom.code == init_dict['code']
    assert dom.serial == init_dict['serial']
    assert dom.host == init_dict['host']
    assert dom.rated == init_dict['rated']
    assert dom.power == init_dict['power']
    assert dom.soc == init_dict['soc']

def test_converter_model_to_dict():
    dom = DomainFactory.create(domain, init_dict)

    assert dom.to_dict() == init_dict

def test_converter_model_comparison():
    dom1 = DomainFactory.create(domain, init_dict)
    dom2 = DomainFactory.create(domain, init_dict)

    assert dom1 == dom2

def test_converter_model_serializer():
    dom = DomainFactory.create(domain, init_dict)
    serializer = SerializerFactory.create(domain)

    json_expected = f"""
        {{
            "code": "{init_dict['code']}",
            "serial": "{init_dict['serial']}",
            "host": "{init_dict['host']}",
            "rated": {init_dict['rated']},
            "power": {init_dict['power']},
            "soc": {init_dict['soc']}
        }}
    """

    json_dom = json.dumps(dom, cls = serializer)

    dict_json_dom = json.loads(json_dom)
    dict_json_expected = json.loads(json_expected)

    assert dict_json_dom == dict_json_expected