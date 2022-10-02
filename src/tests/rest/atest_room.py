from unittest import mock
import json

from ...simulators.domain.simulator_room import room_dicts, rooms
from ...simulators.domain.simulator_hotel import hotel_dicts, hotels

@mock.patch("clean_arquitecture_rentomatic.src.application.backend.rest.room.read_all")
def test_get(mock_use_case, client):

    sims = room_dicts()
    mock_use_case.return_value = sims

    http_response = client.get("/rooms")

    assert json.loads(http_response.data.decode("UTF-8")) == [sims[0]]

    mock_use_case.assert_called()

    assert http_response.status.status_code == 200
    assert http_response.mimetype == "application/json"

