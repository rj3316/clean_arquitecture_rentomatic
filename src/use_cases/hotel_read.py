from ..responses import ResponseSuccess, ResponseFailure, ResponseTypes, build_response_from_invalid_request

class HotelRead:
    @classmethod
    def read(self, repo, request, domain = 'hotel'):
        domain = 'hotel'

        if not request:
            return build_response_from_invalid_request(request)

        try:
            filters = request.filters
            objs = repo.read(domain)
            # objs = repo.read(domain, filters = filters)
            return ResponseSuccess(objs)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)


