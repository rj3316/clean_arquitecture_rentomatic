from ..responses import ResponseSuccess, ResponseFailure, ResponseTypes, build_response_from_invalid_request
from ..exceptions.exception_isnone import ExceptionIsNone

class Read:
    @classmethod
    def read(self, repo, request, domain = None):
        if not request:
            return build_response_from_invalid_request(request)
        try:
            if domain is None: raise ExceptionIsNone('TypeError: <domain> cannot be None')
            filters = request.filters
            objs = repo.read(domain, filters)
            return ResponseSuccess(objs)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)