from flask import Blueprint, request, jsonify
from gpio_api import gpio_controller
from gpio_api.system_state import system_state

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
    
@gpio_blueprint.route('/mode', methods=['POST'])
def set_mode():
    data = request.json
    mode = data.get("mode")
    if mode not in ["manual", "auto", "pid"]:
        return jsonify({"error": "Invalid mode"}), 400
    system_state.mode = mode
    return jsonify({"mode": system_state.mode})

@gpio_blueprint.route('/manual_speed', methods=['POST'])
def set_manual_speed():
    data = request.json
    speed = data.get("speed")
    if speed not in [0, 1, 2, 3]:
        return jsonify({"error": "Invalid speed"}), 400
    system_state.manual_speed = speed
    return jsonify({"manual_speed": system_state.manual_speed})

@gpio_blueprint.route('/pid_params', methods=['POST'])
def set_pid_params():
    data = request.json
    Kp = data.get("Kp")
    Ki = data.get("Ki")
    Kd = data.get("Kd")
    if None in (Kp, Ki, Kd):
        return jsonify({"error": "Missing PID parameters"}), 400
    system_state.pid_params = {"Kp": Kp, "Ki": Ki, "Kd": Kd}
    return jsonify({"pid_params": system_state.pid_params})

@gpio_blueprint.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "mode": system_state.mode,
        "manual_speed": system_state.manual_speed,
        "pid_params": system_state.pid_params,
        "pid_value": system_state.pid_value,
        "status_message": system_state.status_message,
        "target_temperature": system_state.target_temperature    
    })
