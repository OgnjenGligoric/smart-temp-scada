from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from gpio_api.routes import gpio_blueprint
    app.register_blueprint(gpio_blueprint)
    
    return app
