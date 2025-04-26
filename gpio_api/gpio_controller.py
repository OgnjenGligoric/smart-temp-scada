import os
import glob
import time
import RPi.GPIO as GPIO
from config import LED_PINS, SWITCH_PINS

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup LEDs
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setup Switches
for pin in SWITCH_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Temperature Sensor Setup
def setup_sensor():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    return device_file

# Read Raw Temperature Data
def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

# Read Temperature in Celsius
def read_temperature(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    return None

# LED Controls
def turn_on_led(pin):
    if pin not in LED_PINS:
        raise ValueError("Invalid LED Pin")
    GPIO.output(pin, GPIO.HIGH)

def turn_off_led(pin):
    if pin not in LED_PINS:
        raise ValueError("Invalid LED Pin")
    GPIO.output(pin, GPIO.LOW)

# Switch State
def read_switch_state(pin):
    if pin not in SWITCH_PINS:
        raise ValueError("Invalid Switch Pin")
    return GPIO.input(pin)
