import json
from flask import Blueprint, Response

from ....src.repository.repo_factory import RepoFactory
from ....src.use_cases.read_all import ReadAll
from ....src.serializers.room import RoomJsonEncoder
from ....src.simulators.infraestructure.simulator_file import file


blueprint = Blueprint("room", __name__)

# @blueprint.route("/rooms", methods = ['GET'])
def read_all():
    domain = 'room'
    import pdb; pdb.set_trace()

    # repo = RepoFactory('RepoMem')
    config = {'file': file}
    repo = RepoFactory('RepoFile', config)

    result = ReadAll.read_all(repo, domain)

    return Response(
        json.dumps(result, cls = RoomJsonEncoder),
        mimetype = "application/json",
        status = 200,
    )

