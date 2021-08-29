import os

from flask import Flask

from pythonjsonlogger import jsonlogger
import logging.config
import traceback
import time

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False, defaults={'logfilename': 'mylog.log'})

logger.info("Logging started")
                

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        starttime = time.time()
        return 'Hello, World!'
        endtime = time.time()
        duration = endtime - starttime
        logger.info("Route to hello()", extra={"run_duration":duration})
            

    @app.route('/')
    def index():
        starttime = time.time()
        return 'index'
        endtime = time.time()
        duration = endtime - starttime
        logger.info("Route to index()", extra={"run_duration":duration})
    return app
