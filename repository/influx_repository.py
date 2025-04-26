import os
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxRepository:
    def __init__(self, url=None, token=None, org=None, bucket=None):
        self.url = url or os.getenv("INFLUXDB_URL", "http://localhost:8086")
        self.token = token or os.getenv("INFLUXDB_INIT_ADMIN_TOKEN")
        self.org = org or os.getenv("INFLUXDB_INIT_ORG")
        self.bucket = bucket or os.getenv("INFLUXDB_INIT_BUCKET")

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

        # cache the last written values
        self.last_states = {
            "windows_switch": None,
            "present_switch": None,
            "fan_speed": None,
            "temperature": None
        }

    def write_if_changed(self, measurement: str, value: int):
        if self.last_states.get(measurement) != value:
            point = Point(measurement).field("value", value)
            self.write_api.write(bucket=self.bucket, record=point)
            self.last_states[measurement] = value  # Update cached value
        else:
            print(f"[INFO] {measurement} state unchanged, not writing.")

    def write_temperature(self, temperature):
        self.write_if_changed("temperature_data", temperature)

    def write_windows_switch(self, state: int):
        self.write_if_changed("windows_switch", state)

    def write_present_switch(self, state: int):
        self.write_if_changed("present_switch", state)

    def write_fan_speed(self, speed: int):
        self.write_if_changed("fan_speed", speed)


    def read_recent_temperatures(self, time_range="-1h"):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: {time_range})
          |> filter(fn: (r) => r._measurement == "temperature_data")
        '''

        result = self.query_api.query(org=self.org, query=query)

        temperatures = []
        for table in result:
            for record in table.records:
                temperatures.append({
                    "time": record.get_time(),
                    "value": record.get_value()
                })

        return temperatures

    def read_recent_windows_switch(self, time_range="-1h"):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: {time_range})
          |> filter(fn: (r) => r._measurement == "windows_switch")
        '''

        result = self.query_api.query(org=self.org, query=query)

        states = []
        for table in result:
            for record in table.records:
                states.append({
                    "time": record.get_time(),
                    "value": record.get_value()
                })

        return states

    def read_recent_present_switch(self, time_range="-1h"):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: {time_range})
          |> filter(fn: (r) => r._measurement == "present_switch")
        '''

        result = self.query_api.query(org=self.org, query=query)

        states = []
        for table in result:
            for record in table.records:
                states.append({
                    "time": record.get_time(),
                    "value": record.get_value()
                })

        return states

    def read_recent_fan_speed(self, time_range="-1h"):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: {time_range})
          |> filter(fn: (r) => r._measurement == "fan_speed")
        '''

        result = self.query_api.query(org=self.org, query=query)

        speeds = []
        for table in result:
            for record in table.records:
                speeds.append({
                    "time": record.get_time(),
                    "value": record.get_value()
                })

        return speeds

    def close(self):
        self.client.close()
