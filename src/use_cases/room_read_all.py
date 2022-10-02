class ReadAll:
    @classmethod
    def read_all(self, repo, domain = 'room', verbose = False):
        domain = 'room'
        return repo.read(domain, verbose)
# def read_all(self, repo, domain = 'room', verbose = False):
#     domain = 'room'
#     return repo.read(domain, verbose)