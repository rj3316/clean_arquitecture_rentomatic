import json
import uuid

from ...factory.factory_domain import FactoryDomain
from ...factory.factory_serializer import FactorySerializer
from ...factory.factory_simulator import FactorySimulator

def test_room_model_serializer():
    domain = 'converter'

    # Obtenemos la plantilla sobre la que crearemos la entidad de dominio room
    sim_dom = FactorySimulator.create_domain_dicts(domain)[0]

    # Instanciamos room, usando sim_dom de plantilla
    dom = FactoryDomain.create(domain, sim_dom)

    # Construimos lo que esperamos que nos devuelva, suando sim_dom de plantilla
    serializer = FactorySerializer.create(domain)

    json_expected = f"{{"
    for i, (field, value) in enumerate(sim_dom.items()):
        is_str = isinstance(value, str)
        is_uuid = isinstance(value, uuid.UUID)

        json_expected += f"\"{field}\": "

        if is_str or is_uuid: json_expected += "\""
        json_expected += f"{value}"
        if is_str or is_uuid: json_expected += "\""
        if (i+1) != len(sim_dom.keys()): json_expected += ', '
    json_expected += f"}}"
 
    json_dom = json.dumps(dom, cls = serializer)

    # Comparamos las dos estructuras
    dict_json_dom = json.loads(json_dom)
    dict_json_expected = json.loads(json_expected)

    assert dict_json_dom == dict_json_expected
