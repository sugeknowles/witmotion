# witmotion

Find and subscribe to Witmotion WT901BLECL MPU9250 High-Precision 9-axis Gyroscope+Angle 
Works for my use case, your mileage may vary.  Has not been tested with multiple sensors.  MAC discovery (BLESearcher.py) will likely explode, who knows.
Data can be directly converted into a Pandas DataFrame for downstream processing/analytics.
This was a quick effort to collect data for a project from the sensor, and not intended to be complete solution.

Uses Bleak for Bluetooth functionality

# Todo
- requirements.txt
- clean up dead code (zmq publishing.  Didn't need this.)

# Data collection rates
You can select data rates based on your use case.  When connecting to the sensor, pass to the connect() method the rate you want to have the sensor return values.
```python
    witble.connect(WITBLE.RATE_200HZ)
```

# Valid Sample Rates
RATE_POINT2HZ = 0x01
RATE_POINT5HZ = 0x02
RATE_1HZ = 0x03
RATE_2HZ = 0x04
RATE_5HZ = 0x05
RATE_10HZ = 0x06
RATE_20HZ = 0x07
RATE_50HZ = 0x08
RATE_100HZ = 0x09
RATE_200HZ = 0x0B

# Example useage

This example locates a sensor named WITBLE.DEVICE_NAME  ("WT901BLE68"), figures out its MAC and then connects and subscribes at the specified rate.
It collects data for the specified interval and the data can then be read from the data array of the sensor class.

```python
import witble.BLESearcher as searcher
from witble.WITBLE import WITBLE


import sys
import asyncio
import pandas as pd


CONNECTION_TIMEOUT = 30

filename = sys.argv[1]
print(f"Will save captured data as {filename}")
mac = searcher.search(WITBLE.DEVICE_NAME, CONNECTION_TIMEOUT)
print(f"Connecting to {mac}")
witble = WITBLE(mac)
asyncio.run(witble.connect(WITBLE.RATE_200HZ))
print("Calibrating sensor.")
asyncio.run(witble.calibrate())
print("Connected..  Subscribing to data.")
asyncio.run(witble.subscribe(int(sys.argv[2]), False))
print("Subscription complete.")
print(len(witble.data))
asyncio.run(witble.disconnect())
df = pd.DataFrame(witble.data)
df.to_csv(f"imudata/{filename}.csv")
```
