class SystemState:
    def __init__(self):
        self.mode = "manual"  # manual / auto / pid
        self.manual_speed = 0  # 0 = off, 1 = speed1, 2 = speed2, 3 = speed3
        self.pid_params = {"Kp": 1.0, "Ki": 0.1, "Kd": 1.0}
        self.target_temperature = 22.0  # Ideal room temp
        self.pid_value = 0  # Last PID output (0-100%)
        self.status_message = "Message"

system_state = SystemState()
