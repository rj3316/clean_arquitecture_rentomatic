from ...factory.factory_domain import FactoryDomain

serial_1 = '001'
host_1 = '192.168.1.10'
rated_1 = 10
power_1 = 2.5
soc_1 = 78

serial_2 = '002'
host_2 = '192.168.1.11'
rated_2 = 15
power_2 = -1
soc_2 = 46

serial_3 = '003'
host_3 = '192.168.1.12'
rated_3 = 60
power_3 = -56
soc_3 = 98

def converter_dicts():
    converter_1 = {
        "code": "converter_1",
        "serial": serial_1,
        "host": host_1,
        "rated": rated_1,
        "power": power_1,
        "soc": soc_1,
    }
    converter_2 = {
        "code": "converter_2",
        "serial": serial_2,
        "host": host_2,
        "rated": rated_2,
        "power": power_2,
        "soc": soc_2,
    }
    converter_3 = {
        "code": "converter_3",
        "serial": serial_3,
        "host": host_3,
        "rated": rated_3,
        "power": power_3,
        "soc": soc_3,
    }

    ret_val = [converter_1, converter_2, converter_3]
    return ret_val

def converters():
    domain = 'converter'
    dicts = converter_dicts()

    return FactoryDomain.create(domain, dicts)
