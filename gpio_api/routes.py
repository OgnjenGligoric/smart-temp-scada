from flask import Blueprint, request, jsonify
from gpio_api import gpio_controller

gpio_blueprint = Blueprint('gpio', __name__)

# Set up temperature sensor once
try:
    device_file = gpio_controller.setup_sensor()
except Exception as e:
    device_file = None
    print(f"Temperature sensor setup failed: {e}")

@gpio_blueprint.route('/')
def home():
    return "GPIO API is running!"

# Temperature
@gpio_blueprint.route('/temperature', methods=['GET'])
def get_temperature():
    if not device_file:
        return jsonify({"error": "Temperature sensor not available"}), 500
    temp = gpio_controller.read_temperature(device_file)
    return jsonify({"temperature_celsius": temp})

# LED Control
@gpio_blueprint.route('/led/<int:pin>/on', methods=['POST'])
def turn_on_led(pin):
    try:
        gpio_controller.turn_on_led(pin)
        return jsonify({"pin": pin, "state": "on"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@gpio_blueprint.route('/led/<int:pin>/off', methods=['POST'])
def turn_off_led(pin):
    try:
        gpio_controller.turn_off_led(pin)
        return jsonify({"pin": pin, "state": "off"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Switch State
@gpio_blueprint.route('/switch/<int:pin>', methods=['GET'])
def get_switch_state(pin):
    try:
        state = gpio_controller.read_switch_state(pin)
        return jsonify({"pin": pin, "state": "pressed" if state == 0 else "released"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
