from flask import Flask
from gpio_api.daemon_worker import DaemonWorker
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    from gpio_api.routes import gpio_blueprint
    app.register_blueprint(gpio_blueprint)

    return app
