from unittest import mock
import json

from ...simulators.factorysimulator import FactorySimulator

@mock.patch("clean_arquitecture_rentomatic.src.application.backend.rest.hotel_read_all")
def test_get(mock_use_case, client):
    domain = 'hotel'

    sims = FactorySimulator.create_domain_dicts(domain)

    mock_use_case.return_value = sims

    http_response = client.get(f"/{domain}s")

    assert json.loads(http_response.data.decode("UTF-8")) == [sims[0]]

    mock_use_case.assert_called()

    assert http_response.status.status_code == 200
    assert http_response.mimetype == "application/json"

