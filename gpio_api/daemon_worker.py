import threading
import time
from gpio_api import gpio_controller
from gpio_api.system_state import system_state
from gpio_api.gpio_controller import read_switch_state
from config import *
import repository.influx_repository as influx_repository

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, output_limits=(0, 100)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits
        self.integral = 0
        self.last_error = None
        self.influx_client = influx_repository.InfluxRepository()

    def compute(self, current_value, dt):
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = 0 if self.last_error is None else (error - self.last_error) / dt
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        output = max(self.output_limits[0], min(self.output_limits[1], output))
        self.last_error = error
        return output

class DaemonWorker:
    def __init__(self, device_file, interval=5):
        self.device_file = device_file
        self.interval = interval
        self.running = False
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.pid = None

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def _worker(self):
        print("[Daemon] Background worker started.")
        while self.running:
            try:
                temp = gpio_controller.read_temperature(self.device_file)
                self.influx_client.write_temperature(temp)
                print(f"[Daemon] Temp: {temp}°C | Mode: {system_state.mode}")

                # Read door and window states
                door_state = read_switch_state(SWITCH1_PIN)
                window_state = read_switch_state(SWITCH2_PIN)

                # NEW: Check if door or window is open
                if door_state == 0 or window_state == 0:
                    print("[Daemon] Door or window open. Pausing system.")
                    # Turn off all fan speeds
                    gpio_controller.turn_off_led(PIN1)
                    gpio_controller.turn_off_led(PIN2)
                    gpio_controller.turn_off_led(PIN3)

                    # Update system state if needed
                    system_state.current_speed = 0
                    system_state.pid_value = 0
                    system_state.status_message = "Paused (door/window open)"
                else:
                    # Normal operation
                    if system_state.mode == "manual":
                        self._handle_manual()
                    elif system_state.mode == "auto":
                        self._handle_auto(temp)
                    elif system_state.mode == "pid":
                        self._handle_pid(temp)

                    system_state.status_message = "Running normally"

                time.sleep(self.interval)

            except Exception as e:
                print(f"[Daemon] Error: {e}")
                time.sleep(5)


    def _handle_manual(self):
        self._set_speed(system_state.manual_speed)

    def _handle_auto(self, temp):
        deviation = abs(temp - system_state.target_temperature)
        if deviation < 2:
            speed = 0
        elif 2 <= deviation <= 5:
            speed = 2
        else:
            speed = 3
        self._set_speed(speed)

    def _handle_pid(self, temp):
        if not self.pid:
            params = system_state.pid_params
            self.pid = PIDController(
                params["Kp"], params["Ki"], params["Kd"],
                setpoint=system_state.target_temperature
            )
        output = self.pid.compute(temp, self.interval)
        system_state.pid_value = output
        print(f"[Daemon] PID output: {output:.2f}%")

    def _set_speed(self, speed):
        # Turn off all LEDs first
        gpio_controller.turn_off_led(17)
        gpio_controller.turn_off_led(27)
        gpio_controller.turn_off_led(22)
        
        if speed == 1:
            gpio_controller.turn_on_led(17)
        elif speed == 2:
            gpio_controller.turn_on_led(27)
        elif speed == 3:
            gpio_controller.turn_on_led(22)
