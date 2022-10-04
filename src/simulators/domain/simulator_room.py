from ...factory.factory_domain import FactoryDomain

size_1 = 215
price_1 = 39
longitude_1 = -0.09998975
latitude_1 = 51.75436293

size_2 = 405
price_2 = 66
longitude_2 = 0.18228006
latitude_2 = 51.74640997

size_3 = 56
price_3 = 60
longitude_3 = 0.27891577
latitude_3 = 51.45994069

size_4 = 93
price_4 = 48
longitude_4 = 0.33894476
latitude_4 = 51.39916678


def room_dicts():
    room_1 = {
        "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "size": size_1,
        "price": price_1,
        "longitude": longitude_1,
        "latitude": latitude_1,
    }

    room_2 = {
        "code": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        "size": size_2,
        "price": price_2,
        "longitude": longitude_2,
        "latitude": latitude_2,
    }

    room_3 = {
        "code": "913694c6-435a-4366-ba0d-da5334a611b2",
        "size": size_3,
        "price": price_3,
        "longitude": longitude_3,
        "latitude": latitude_3,
    }

    room_4 = {
        "code": "eed76e77-55c1-41ce-985d-ca49bf6c0585",
        "size": size_4,
        "price": price_4,
        "longitude": longitude_4,
        "latitude": latitude_4,
    }
    ret_val = [room_1, room_2, room_3, room_4]
    return ret_val

def rooms():
    domain = 'room'
    dicts = room_dicts()

    return FactoryDomain.create(domain, dicts)
