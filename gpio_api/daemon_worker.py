import threading
import os
import time
from gpio_api.system_state import system_state
from config import *
from repository.influx_repository import InfluxRepository
import paho.mqtt.client as mqtt
import json
import asyncio
import websockets


class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, output_limits=(-100, 100)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits
        self.integral = 0
        self.last_error = None
        

    def compute(self, current_value, dt):
        error = self.setpoint - current_value
        print(f"[PID] Error: {error:.2f} | Setpoint: {self.setpoint:.2f} | Current: {current_value:.2f}")
        self.integral += error * dt
        derivative = 0 if self.last_error is None else (error - self.last_error) / dt
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        output = max(self.output_limits[0], min(self.output_limits[1], output))
        self.last_error = error
        return abs(output)

class DaemonWorker:
    def __init__(self):
        self.interval = 5  # seconds
        self.running = False
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.pid = None
        self.influx_client = InfluxRepository()
        self.client = mqtt.Client()
        self.client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')), 60)
        self.client.on_message = self.on_message
        self.client.subscribe(f"{os.getenv('DEVICE_ID')}/status")
        self.client.loop_start()
        self.device_id = None
        self.current_temperature = None
        self.switch_window = None
        self.switch_someone_present = None
        self.leds_on = None
        self.websocket_uri = "ws://localhost:8000/" 
        self.websocket = None

    def on_message(self, client, userdata, msg):
        try:
            status = json.loads(msg.payload.decode())
            print(status)
            self.device_id = status.get("device_id")
            self.current_temperature = status.get("temperature_c")
            self.leds_on = status.get("leds_on")
            switches = status.get("switches", {})
            self.switch_window = switches.get("switch_1")
            self.switch_someone_present = switches.get("switch_2")
        except Exception as e:
            print(f"Error handling message: {e}")

    def command(self, action, pin):
        return {"action": action, "pin": pin}

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
                temp = self.current_temperature
                self.influx_client.write_temperature(temp)
                self.influx_client.write_windows_switch(self.switch_window)
                self.influx_client.write_present_switch(self.switch_someone_present)
                self.influx_client.write_fan_speed(self.leds_on)
                self.publish_to_websocket()


                print(f"[Daemon] Temp: {temp}°C | Mode: {system_state.mode}")

                # Read door and window states
                door_state = self.switch_someone_present
                window_state = self.switch_window

                # NEW: Check if door or window is open
                if door_state == "off" or window_state == "off":
                    print("[Daemon] Door or window open. Pausing system.")
                    # Turn off all fan speeds
                    self.set_led("turn_off_led", [LED1_PIN, LED2_PIN, LED3_PIN])

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
        pass
        # self._set_speed(system_state.manual_speed)

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
            print(f"[Daemon] PID params: {params}")
            self.pid = PIDController(
                params["Kp"], params["Ki"], params["Kd"],
                setpoint=system_state.target_temperature
            )
            print(f"[Daemon] PID setpoint: {system_state.target_temperature}°C")

        output = self.pid.compute(temp, self.interval)
        system_state.pid_value = output
        print(f"[Daemon] PID output: {output:.2f}%")

    def _set_speed(self, speed):
        # Turn off all LEDs first
        self.set_led("turn_off_led", [LED1_PIN, LED2_PIN, LED3_PIN])

        if speed == 1:
            self.set_led("turn_on_led", [LED1_PIN])
        elif speed == 2:
            self.set_led("turn_on_led", [LED1_PIN, LED2_PIN])
        elif speed == 3:
            self.set_led("turn_on_led", [LED1_PIN, LED2_PIN, LED3_PIN])
    
    def set_led(self, action, pins):
            """Helper to send LED commands easily."""
            for pin in pins:
                self.client.publish(
                    f"{os.getenv('DEVICE_ID')}/command",
                    json.dumps(self.command(action, pin))
                )

    def get_switch(self, pin):
        if pin == 23:
            return self.switch_window
        elif pin == 24:
            return self.switch_someone_present
        else:
            return None
    
    async def _connect_websocket(self):
        """Establish a WebSocket connection."""
        try:
            self.websocket = await websockets.connect(self.websocket_uri)
            print("[WebSocket] Connected to server.")
        except Exception as e:
            print(f"[WebSocket] Error connecting: {e}")

    async def _send_to_websocket(self, message):
        """Send message to the WebSocket server."""
        if self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
                print(f"[WebSocket] Message sent: {message}")
            except Exception as e:
                print(f"[WebSocket] Error sending message: {e}")

    def publish_to_websocket(self):
        """Publish relevant data to the WebSocket server."""
        if self.websocket:
            data = {
                "device_id": self.device_id,
                "temperature": self.current_temperature,
                "leds_on": self.leds_on,
                "switch_window": self.switch_window,
                "switch_someone_present": self.switch_someone_present,
                "pid_value": system_state.pid_value,
                "status_message": system_state.status_message,
            }
            # Send the data asynchronously to the WebSocket server
            asyncio.run(self._send_to_websocket(data))
        else:
            print("[WebSocket] WebSocket not connected!")
