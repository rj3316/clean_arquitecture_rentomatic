import json
from flask import Blueprint, Response, request

from ....use_cases.read import Read
from ....requests.read_request import BuilderReadRequest
from ....repository.repo_factory import RepoFactory
from ....serializers.factoryserializer import SerializerFactory

from ....simulators.factorysimulator import FactorySimulator

blueprint = Blueprint("domain", __name__)

@blueprint.route("/domains", methods = ['GET'])
def read():
    # Identificamos la entidad de dominio que se ha pedido
    domain = request.args.get('domain')
    # if domain is None: domain = 'room'

    # Obtenemos el repositorio (repo_selector = ...)
    # 0: RAM
    # 1: File
    # 2: SQL    
    repo_selector = 1
    if repo_selector == 0:
        repo_detail = 'RepoMem'
    elif repo_selector == 1:
        repo_detail = 'RepoSql'
    elif repo_selector == 2:
        repo_detail = 'RepoFile'
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = RepoFactory.create(repo_detail, config)

    # Aplicamos el UseCase
    req = BuilderReadRequest.build_read_request(request.args)

    # Aplicamos el UseCase
    result = Read.read(repo, req, domain)

    serializer = SerializerFactory.create(domain)
    return Response(
        json.dumps(result.value, cls = serializer),
        mimetype = "application/json",
        status = 200,
    )
