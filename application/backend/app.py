from flask import Flask

def create_app(config_name = None):
    if config_name is None: config_name = 'testing'

    app = Flask(__name__)

    config_module = f"clean_arquitecture_rentomatic.application.backend.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    return app