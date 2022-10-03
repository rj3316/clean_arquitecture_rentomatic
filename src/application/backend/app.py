from flask import Flask
from .rest.room_read_endpoint import blueprint as blueprint_room
from .rest.hotel_read_endpoint import blueprint as blueprint_hotel

def create_app(config_name = None):
    if config_name is None: config_name = 'testing'

    app = Flask(__name__)

    config_module = f"clean_arquitecture_rentomatic.src.application.backend.config.Config{config_name.capitalize()}"
    app.config.from_object(config_module)
    
    app.register_blueprint(blueprint_room)
    app.register_blueprint(blueprint_hotel)

    return app