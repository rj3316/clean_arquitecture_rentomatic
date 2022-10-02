import os

from .src.application.backend.app import create_app

try: flask_config = os.environ["FLASK_CONFIG"]
except: flask_config = "testing"

app = create_app(flask_config)
