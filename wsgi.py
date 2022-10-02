import os
from flask import Flask

# from application.backend.app import create_app
# from application.backend.rest.room import read_all

# from application.backend.rest.room import read_all
from src.rest.room import read_all

# from .application.backend.rest.room import read_all

if __name__ == '__main__':
    pause = True

    os.environ["FLASK_CONFIG"] = 'testing'

    # app = create_app(config_name = os.environ["FLASK_CONFIG"])
    app = Flask(__name__)

    app.add_url_rule('/domains', view_func = read_all, methods = ['GET'])

    app.run()