from unittest import mock
import json

from flask import Blueprint

from ...simulators.domain.simulator_room import rooms, room_dicts

@mock.patch("application.backend.rest.room.room_list")
def test_get(mock_use_case, client):
    sim_rooms = room_dicts()
    mock_use_case.return_value = rooms

    http_response = client.get("/rooms")

    assert json.loads(http_response.data.decode("UTF-8")) == [sim_rooms[0]]

    mock_use_case.assert_called()

    assert http_response.status.status_code == 200
    assert http_response.mimetype == "application/json"



# blueprint = Blueprint('room', __name__)

# @blueprint.route('/room', methods = ['GET'])
# def room_list():
#     [LOGIC]
#     return Response([JSON DATA], 
#                     mimetype = 'application/json',
#                     status=[STATUS])