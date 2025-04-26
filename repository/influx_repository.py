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

    def write_temperature(self, temperature):
        point = Point("temperature_data").field("value", temperature)
        self.write_api.write(bucket=self.bucket, record=point)

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

    # ====== NEW METHODS ======

    def write_windows_switch(self, state: int):
        point = Point("windows_switch").field("value", state)
        self.write_api.write(bucket=self.bucket, record=point)

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

    def write_present_switch(self, state: int):
        point = Point("present_switch").field("value", state)
        self.write_api.write(bucket=self.bucket, record=point)

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

    def write_fan_speed(self, speed: int):
        point = Point("fan_speed").field("value", speed)
        self.write_api.write(bucket=self.bucket, record=point)

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
