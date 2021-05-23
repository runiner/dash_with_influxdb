from typing import Optional, Dict, List

import influxdb_client
from influxdb_client.client.write_api import WriteOptions


class Storage:
    def __init__(self):
        # TODO: move configuration to .env/variables
        self.bucket = "my-bucket"
        self.org = "my-org"
        self.token = "my-token"
        self.url = "http://influx_db_service:8086"

        self.client = influxdb_client.InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )
        self.query_api = self.client.query_api()

    def write_batch(self, batch: List[Dict], tags: Optional[Dict] = None):
        write_api = self.client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=1_000))
        buf = []
        for item in batch:
            p = influxdb_client.Point("test_data").field("price", item["value"])\
                .time(item["timestamp"], write_precision="ms")
            if tags:
                for k, v in tags.items():
                    p.tag(k, v)  # TODO: needs sanity checking for tag/value syntax
            buf.append(p)
            write_api.write(bucket=self.bucket, record=p)

        write_api.close()

    def query(self, start_dt: str, tags: Optional[Dict] = None):
        query = f"""from(bucket: "{self.bucket}")
             |> range(start: {start_dt})
            """
        if tags:
            for k, v in tags.items():
                query += f' |> filter(fn: (r) => r.{k} == "{v}")'  # TODO: needs sanity checking for tag/value syntax
        result = self.query_api.query(query)
        flat_res = [(r.get_field(), r.get_value(), r.get_time()) for t in result for r in t.records]
        return flat_res
