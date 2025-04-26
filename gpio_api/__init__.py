from flask import Flask
from gpio_api import gpio_controller
from gpio_api.daemon_worker import DaemonWorker

daemon = None

def create_app():
    global daemon
    app = Flask(__name__)

    from gpio_api.routes import gpio_blueprint
    app.register_blueprint(gpio_blueprint)

    # Set up temperature sensor once
    try:
        device_file = gpio_controller.setup_sensor()
        daemon = DaemonWorker(device_file=device_file, interval=5)
        daemon.start()
    except Exception as e:
        print(f"[App] Temperature sensor setup failed: {e}")

    return app
