from ..responses import ResponseSuccess

def test_reponse_success_is_true():
    assert bool(ResponseSuccess()) is True