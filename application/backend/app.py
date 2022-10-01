from flask import Flask

def create_app(config_name):
    app = Flask(__name__)

    config_module = f".config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    return app