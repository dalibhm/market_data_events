from flask import Flask

from ib_gateway.log_init import init_log
from ib_gateway.services import bootstrap


def create_app(config_name):
    app = Flask(__name__)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    with app.app_context():
        init_log()
        bus = bootstrap.bootstrap()

    return app
