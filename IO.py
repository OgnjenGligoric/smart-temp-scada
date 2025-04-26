import os
import glob
import time
import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Config
LED_PINS = [17, 27, 22]
SWITCH_PINS = [23, 24]
MQTT_BROKER = "172.20.10.3"   # change to your broker IP
MQTT_PORT = 1883
DEVICE_ID = "raspberry_pi_1"
PUBLISH_INTERVAL = 5  # seconds


# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in SWITCH_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Temperature Sensor Setup
def setup_sensor():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    return device_folder + '/w1_slave'

def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temperature(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        return float(lines[1][equals_pos + 2:]) / 1000.0
    return None

# Count LEDs that are ON
def count_leds_on():
    return sum(GPIO.input(pin) for pin in LED_PINS)

# Get switch states
def get_switch_states():
    return {
        f"switch_{i+1}": "on" if GPIO.input(pin) == 0 else "off"
        for i, pin in enumerate(SWITCH_PINS)
    }

def on_message(client, userdata, msg):
    try:
        command = json.loads(msg.payload.decode())
        print(command)
        action = command.get("action")
        pin = command.get("pin")

        if action == "turn_on_led" and pin in LED_PINS:
           turn_on_led(pin)

        elif action == "turn_off_led" and pin in LED_PINS:
            turn_off_led(pin)

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error handling message: {e}")


def turn_on_led(pin):
    if pin not in LED_PINS:
        raise ValueError("Invalid LED Pin")
    GPIO.output(pin, GPIO.HIGH)

def turn_off_led(pin):
    if pin not in LED_PINS:
        raise ValueError("Invalid LED Pin")
    GPIO.output(pin, GPIO.LOW)

# MQTT Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.on_message = on_message
client.subscribe(f"{DEVICE_ID}/command")
client.loop_start()

# Main Loop
def main():
    device_file = setup_sensor()

    try:
        while True:
            payload = {
                "device_id": DEVICE_ID,
                "temperature_c": read_temperature(device_file),
                "leds_on": count_leds_on(),
                "switches": get_switch_states(),
                "timestamp": int(time.time())
            }

            client.publish(f"{DEVICE_ID}/status", json.dumps(payload))

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
