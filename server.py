# from app import create_app
# Flask modules
from flask import Flask
from werkzeug.serving import run_simple
from flask_bcrypt import Bcrypt
from app.extensions.responses import response_base
# Other modules
import os


def create_app(debug: bool = False):
    # Check if debug environment variable was passed
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", True)
    if FLASK_DEBUG:
        debug = FLASK_DEBUG

    # Create the Flask application instance
    app = Flask(
        __name__,
        template_folder="./templates",
        static_folder="./static",
        static_url_path="/",
    )

    # Set current_app context
    app.app_context().push()

    if debug:
        from app.config.dev import DevConfig

        app.config.from_object(DevConfig)
    else:
        from app.config.prod import ProdConfig

        app.config.from_object(ProdConfig)

    # Uncomment to enable logger
    # from app.utils.logger import setup_flask_logger
    # setup_flask_logger()

    # Initialize extensions
    from app.extensions import db
    # print(db.db.ini)
    db.db.init_app(app)

    # Import all models and Create database tables
    # from app import models

    # db.create_all()

    # Register blueprints or routes

    # app.register_blueprint(auth)

    # Global Ratelimit Checker
    # this is used because auto_check is set to 'False'
    # app.before_request(lambda: limiter.check())

    return app


app = create_app(debug=True)
bcrypt = Bcrypt(app)
if __name__ == "__main__":
    from app.routes.auth import *
    from app.routes.property import *

    @app.errorhandler(Exception)
    def server_error(err):
        app.logger.exception(err)
        return response_base("Server Error", 500)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.run()
    run_simple(
        application=app,
        hostname="localhost",
        port=5000,
        use_debugger=True,
        use_reloader=True,
    )
