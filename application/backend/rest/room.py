import json
from unittest import result
from flask import Blueprint, Response

from ....src.repository.repo_factory import RepoFactory
from ....src.use_cases.read_all import read_all #room_list_use_case #read_all
from ....src.serializers.room import RoomJsonEncoder
from ....src.simulators.domain.simulator_room import rooms, room_dicts

blueprint = Blueprint("room", __name__)

@blueprint.route("/rooms", methods = ['GET'])
def room_list():
    domain = 'room'

    repo = RepoFactory('RepoMem')

    sim_rooms = room_dicts()
    repo.write(domain, data = sim_rooms)
    result = read_all(repo, domain)

    return Response(
        json.dumps(result, cls = RoomJsonEncoder),
        mimetype = "application/json",
        status = 200,
    )
