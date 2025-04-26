from flask import Flask, jsonify
import os
import glob
import time
import RPi.GPIO as GPIO

PIN1 = 17
PIN2 = 27
PIN3 = 22

'''
    Senzor temperature
    Koriscenje: 
        1) pozvati sensor = setup_sensor()
        2) pozvati temperatura = read_temperature(sensor)
'''
def setup_sensor():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]  
    device_file = device_folder + '/w1_slave'
    return device_file

def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temperature(device_file):
    lines = read_temp_raw(device_file)
    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    return None




'''
    LED
    Ukljuci LED: turn_on_led(LED_koji_se_ukljucuje)
    Ugasi LED: turn_off_led(LED_koji_se_gasi)
    LED1 je na Pinu 17 ukoliko je dobro povezano
    LED2 je na Pinu 27 ukoliko je dobro povezano
    LED3 je na Pinu 22 ukoliko je dobro povezano
    
    Pinovi u programu se razlikuju po oznaci od onih na raspberry plocici
'''
def turn_on_led(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turn_off_led(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)




'''
    Prekidaci
    Procitaj stanje prekidaca: stajne_prekidaca = read_switch_state(prekidac)
    Prekidac1 je na pinu 23 ukoliko je dobro povezano
    Prekidac2 je na pinu 24 ukoliko je dobro povezano
    
    Pinovi u programu se razlikuju po oznaci od onih na raspberry plocici
'''
def read_switch_state(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
    return GPIO.input(pin)


'''
    demo funkcija
'''
if __name__ == "__main__":
    device_file = setup_sensor()
    for i in range(3):
        t = 0.3
        temperature = read_temperature(device_file)
        print('temperatura: ', temperature)
        turn_on_led(PIN1)
        time.sleep(t)
        turn_off_led(PIN1)
        turn_on_led(PIN2)
        time.sleep(t)
        turn_off_led(PIN2)
        turn_on_led(PIN3)
        time.sleep(t)
        turn_off_led(PIN3)
        print(read_switch_state(23))
        print(read_switch_state(24))


    try:
    # Try to import Flask
        from flask import Flask

        # Create a simple Flask app
        app = Flask(__name__)

        # Define a route
        @app.route('/')
        def hello_world():
            return 'Flask is working!'

        # Run the app
        app.run(host='0.0.0.0', port=5000)

    except ImportError:
        print("Flask is not installed.")