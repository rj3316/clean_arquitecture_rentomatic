from .builder_read_request import BuilderReadRequest

class BuilderRoomReadRequest(BuilderReadRequest):
    def _get_accepted_filters(self):
        return ['code__eq', 'price__eq', 'price__lt', 'price__gt']
