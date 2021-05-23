import csv
import logging
from datetime import datetime, timedelta


class StockData:
    def __init__(self, filename: str):
        self._seconds = None
        self._data = None
        self._filename = filename

        self._read_csv(filename)

    def _read_csv(self, filename):
        res = []
        with open(filename, "rt") as f:
            reader = csv.reader(f)
            _header = next(reader, None)
            for row in reader:
                try:
                    seconds = int(row[0])
                    value = float(row[1])
                except (LookupError, ValueError) as ex:
                    logging.error(f"Error reading CSV file, row '{row}', parsing error: {ex}")
                    raise ex
                res.append([seconds, value])
                if self._seconds is None or self._seconds < seconds:
                    self._seconds = seconds
        self._data = res

    def get_length(self):
        return self._seconds

    def get_samples_since(self, timestamp: datetime):
        for row in self._data:
            yield {
                "timestamp": timestamp + timedelta(seconds=row[0]),
                "value": row[1],
            }
