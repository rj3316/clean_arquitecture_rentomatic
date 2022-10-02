import json
from flask import Blueprint, Response, request

from ..repository.repo_factory import RepoFactory
from ..use_cases.read_all import ReadAll
from ..serializers.factoryserializer import SerializerFactory

from ..simulators.infraestructure.simulator_file import file
from ..simulators.infraestructure.simulator_mysql import mysql

blueprint = Blueprint("room", __name__)

@blueprint.route("/domains", methods = ['GET'])
def read_all():
    domain = request.args.get('domain')

    if domain is None: domain = 'room'

    # config = {'file': file}
    # repo = RepoFactory.create('RepoFile', config)

    config = {'ddbb_config': mysql}
    repo = RepoFactory.create('RepoSql', config)

    result = ReadAll.read_all(repo, domain)
    
    serializer = SerializerFactory.create(domain)
    return Response(
        json.dumps(result, cls = serializer),
        mimetype = "application/json",
        status = 200,
    )

