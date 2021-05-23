from datetime import datetime, timedelta, timezone

import pause

from stock_data import StockData
from repository import Storage

filename = "data.csv"

if __name__ == "__main__":
    source = StockData(filename)
    time_length = timedelta(seconds=source.get_length())  # length of dataset in seconds

    storage = Storage()

    start_time = datetime.now(timezone(timedelta(hours=0), "UTC"))
    i = 0
    # Endless loop pushing new data
    while True:
        storage.write_batch(source.get_samples_since(start_time + (i-1) * time_length))
        i += 1
        pause.until(start_time + i * time_length)
