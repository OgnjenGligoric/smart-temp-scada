from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxRepository:
    def __init__(self, url, token, org, bucket):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

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

    def close(self):
        self.client.close()