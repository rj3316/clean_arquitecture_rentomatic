import json
from flask import Blueprint, Response

from ....use_cases.hotel_read_all import ReadAll
from ....repository.repo_factory import RepoFactory
from ....serializers.factoryserializer import SerializerFactory

from ....simulators.infraestructure.simulator_file import file
from ....simulators.infraestructure.simulator_mysql import mysql

blueprint = Blueprint("hotel", __name__)

@blueprint.route("/hotels", methods = ['GET'])
def read_all():
    # Identificamos la entidad de dominio que se ha pedido
    domain = 'hotel'

    # Obtenemos el repositorio (repo_selector = ...)
    # 0: RAM
    # 1: File
    # 2: SQL

    repo_selector = 1
    if repo_selector == 0:
        config = None
        repo_detail = 'RepoMem'
    elif repo_selector == 1:
        config = {'ddbb_config': mysql}
        repo_detail = 'RepoSql'
    elif repo_selector == 2:
        config = {'file': file}
        repo_detail = 'RepoFile'
    repo = RepoFactory.create(repo_detail, config)

    # Aplicamos el UseCase
    result = ReadAll.read_all(repo, domain)

    serializer = SerializerFactory.create(domain)
    return Response(
        json.dumps(result, cls = serializer),
        mimetype = "application/json",
        status = 200,
    )

