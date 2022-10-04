import uuid
import json

from ...domain.room import Room
from ...factory.factory_domain import FactoryDomain
from ...factory.factory_serializer import FactorySerializer
from ...factory.factory_simulator import FactorySimulator

domain = 'room'

init_dict = FactorySimulator.create_domain_dicts(domain)[0]
init_dict['code'] = uuid.uuid4()

def test_room_model_init():
    dom = Room()
    for key, value in init_dict.items():
        setattr(dom, key, value)

    for key, value in init_dict.items():
        assert getattr(dom, key) == value

def test_room_model_from_dict():
    dom = FactoryDomain.create(domain, init_dict)

    for key, value in init_dict.items():
        assert getattr(dom, key) == value

def test_room_model_to_dict():
    dom = FactoryDomain.create(domain, init_dict)

    assert dom.to_dict() == init_dict

def test_room_model_comparison():
    dom1 = FactoryDomain.create(domain, init_dict)
    dom2 = FactoryDomain.create(domain, init_dict)

    assert dom1 == dom2

def test_room_model_serializer():
    dom = FactoryDomain.create(domain, init_dict)
    serializer = FactorySerializer.create(domain)

    json_expected = f"{{\n"
    for i, (key, value) in enumerate(init_dict.items()):
        is_str = isinstance(value, str)
        is_uuid = isinstance(value, uuid.UUID)

        json_expected += f"\"{key}\": "
        if is_str or is_uuid: json_expected += "\""
        json_expected += f"{value}"
        if is_str or is_uuid: json_expected += "\""
        if (i+1) < len(init_dict.keys()): json_expected += ','
        json_expected += '\n'
    json_expected += f"}}"

    json_dom = json.dumps(dom, cls = serializer)

    dict_json_dom = json.loads(json_dom)
    dict_json_expected = json.loads(json_expected)

    assert dict_json_dom == dict_json_expected