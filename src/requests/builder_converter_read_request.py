from .builder_read_request import BuilderReadRequest

class BuilderConverterReadRequest(BuilderReadRequest):
    def _get_accepted_filters(self):
        return ['code__eq', 
                'serial__eq', 'serial__lt', 'serial__gt', 
                'rated__eq', 'rated__lt', 'rated__gt', 
                'host__eq', 'host__lt', 'host__gt', 
                'power__eq', 'power__lt', 'power__gt', 
                'soc__eq', 'soc__lt', 'soc__gt'
        ]
