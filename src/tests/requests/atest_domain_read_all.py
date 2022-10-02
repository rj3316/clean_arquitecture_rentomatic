from ...requests.DomainReadAllRequest import DomainReadAllRequest

def test_build_domain_read_all_request_without_parameters():
    request = DomainReadAllRequest()


def test_build_domain_read_all_request_from_empty_dict():
    request = DomainReadAllRequest.from_dict()

    assert bool(request) is True
    