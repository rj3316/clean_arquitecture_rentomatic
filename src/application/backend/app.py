from flask import Flask
from .rest.domain import blueprint

def create_app(config_name = None):  
    if config_name is None: config_name = 'testing'

    app = Flask(__name__)

    config_module = f"clean_arquitecture_rentomatic.src.application.backend.config.Config{config_name.capitalize()}"
    app.config.from_object(config_module)
    
    app.register_blueprint(blueprint)

    return app