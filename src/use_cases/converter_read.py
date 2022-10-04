from ..responses import ResponseSuccess, ResponseFailure, ResponseTypes, build_response_from_invalid_request

class ConverterRead:
    @classmethod
    def read(self, repo, request, domain = 'converter'):
        domain = 'converter'

        if not request:
            return build_response_from_invalid_request(request)
        try:
            filters = request.filters
            objs = repo.read(domain, filters)
            return ResponseSuccess(objs)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)