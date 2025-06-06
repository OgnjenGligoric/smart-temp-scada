from flask import Blueprint, request, jsonify, current_app
from gpio_api.system_state import system_state
from gpio_api.daemon_worker import DaemonWorker
from repository.influx_repository import InfluxRepository

gpio_blueprint = Blueprint('gpio', __name__)

daemon = DaemonWorker()
influx = InfluxRepository()
daemon.start()

@gpio_blueprint.route('/')
def home():
    return "GPIO API is running!"

# Temperature
@gpio_blueprint.route('/temperature', methods=['GET'])
def get_temperature():
    temp = daemon.temperature
    return jsonify({"temperature_celsius": temp})

# LED Control
@gpio_blueprint.route('/led/<int:pin>/on', methods=['POST'])
def turn_on_led(pin):
    try:
        daemon.set_led("turn_on_led", [pin])
        return jsonify({"pin": pin, "state": "on"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@gpio_blueprint.route('/led/<int:pin>/off', methods=['POST'])
def turn_off_led(pin):
    try:
        daemon.set_led("turn_off_led", [pin])
        return jsonify({"pin": pin, "state": "off"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Switch State
@gpio_blueprint.route('/switch/<int:pin>', methods=['GET'])
def get_switch_state(pin):
    try:
        state = daemon.get_switch(pin)
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
    print(f"[ROUTING] Received PID params: {request.json}")
    data = request.json
    print(f"[ROUTING] Received PID params: {data}")
    Kp = data.get("kp")
    Ki = data.get("ki")
    Kd = data.get("kd")
    target_temp = data.get("target_temp")
    if None in (Kp, Ki, Kd):
        return jsonify({"error": "Missing PID parameters"}), 400
    system_state.pid_params = {"Kp": Kp, "Ki": Ki, "Kd": Kd}
    system_state.target_temperature = target_temp
    print(f"[ROUTING] Updated PID params: {system_state.pid_params}")
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

@gpio_blueprint.route('/influx/temperature', methods=['GET'])
def get_recent_temperatures():
    try:
        temperatures = influx.read_recent_temperatures()
        return jsonify(temperatures), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get recent windows switch states
@gpio_blueprint.route('/influx/windows_switch', methods=['GET'])
def get_recent_windows_switch():
    try:
        states = influx.read_recent_windows_switch()
        return jsonify(states), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get recent present switch states
@gpio_blueprint.route('/influx/present_switch', methods=['GET'])
def get_recent_present_switch():
    try:
        states = influx.read_recent_present_switch()
        return jsonify(states), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get recent fan speeds
@gpio_blueprint.route('/influx/fan_speed', methods=['GET'])
def get_recent_fan_speed():
    try:
        speeds = influx.read_recent_fan_speed()
        return jsonify(speeds), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
