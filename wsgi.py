import os
import pdb

from .application.backend.app import create_app

if __name__ == '__main__':
    pdb.set_trace()
    app = create_app(config = os.environ["FLASK_CONFIG"])