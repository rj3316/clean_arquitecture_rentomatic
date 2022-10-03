from ..responses import ResponseSuccess

class ReadAll:
    @classmethod
    def read_all(self, repo, request, domain = 'hotel'):
        domain = 'hotel'
        objs = repo.read(domain)

        return ResponseSuccess(objs)


