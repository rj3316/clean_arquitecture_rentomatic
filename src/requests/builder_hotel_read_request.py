from .builder_read_request import BuilderReadRequest

class BuilderHotelReadRequest(BuilderReadRequest):
    def _get_accepted_filters(self):
        return ['code__eq', 'name__eq', 'rooms__eq', 'rooms__lt', 'rooms__gt']
