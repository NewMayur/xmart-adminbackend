# from app import create_app
# Flask modules
from flask import Flask, render_template, send_from_directory
from werkzeug.serving import run_simple
from flask_bcrypt import Bcrypt
from app.extensions.responses import response_base
from flask_cors import CORS
from flask_jwt_extended import JWTManager

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
    CORS(app)
    JWTManager(app)
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
    from app.routes.buildings import *
    from app.routes.master import *
    from app.routes.rooms import *
    from app.routes.guest import *
    from app.routes.experience import *
    from app.routes.rooms import *
    from datetime import datetime
    #import pytz

    FLUTTER_WEB_APP = "templates"

    test = True
    # @app.route("/testupdate/")
    # def testupdate():
    #     # current_time = datetime.now(pytz.timezone('Asia/Calcutta'))
    #     formatted_time = current_time.strftime('%H:%M:%S')
    #     global test
    #     test = formatted_time
    #     return "HI"
    @app.route("/teststatus/")
    def teststatus():
        global test
        return str(test)

    @app.route("/web/")
    def render_page_web():
        return render_template("/index.html")

    @app.route("/web/<path:name>")
    def return_flutter_doc(name):

        datalist = str(name).split("/")
        DIR_NAME = FLUTTER_WEB_APP

        if len(datalist) > 1:
            for i in range(0, len(datalist) - 1):
                DIR_NAME += "/" + datalist[i]

        return send_from_directory(DIR_NAME, datalist[-1])
        

    @app.errorhandler(Exception)
    def server_error(err):
        app.logger.exception('An error occurred: %s', str(err), extra={'status': 500})
        return response_base("Server Error", 500)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    run_simple(
        application=app,
        hostname=os.environ.get("BASE_IP", "0.0.0.0"),
        port=int(os.environ.get("PORT")),
        use_debugger=True,
        use_reloader=True,
    )
