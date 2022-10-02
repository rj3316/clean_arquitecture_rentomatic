from ...domain.domainfactory import DomainFactory

nif_1 = 'B12345678'
name_1 = 'Hoteles Paco'
rooms_1 = 10

nif_2 = 'B87654321'
name_2 = 'NH Torrelavega'
rooms_2 = 21

def hotel_dicts():
    hotel_1 = {
        "code": "z854275d-gh0f-1f65-8bj8-56679dffp8y7",
        "nif": nif_1,
        "name": name_1,
        "rooms": rooms_1,
    }

    hotel_2 = {
        "code": "nm273191-eeff-ar72-j081-e0bdc0ec7ui9",
        "nif": nif_2,
        "name": name_2,
        "rooms": rooms_2,
    }
    ret_val = [hotel_1, hotel_2]
    return ret_val

def hotels():
    domain = 'hotel'
    dicts = hotel_dicts()

    return DomainFactory.create(domain, dicts)
