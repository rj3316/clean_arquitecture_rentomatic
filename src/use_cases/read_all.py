from .use_case import UseCase

class ReadAll(UseCase):
    @classmethod
    def read_all(self, repo, domain, verbose = False):
        return repo.read(domain, verbose)