# witmotion
Find and subscribe to Witmotion WT901BLECL MPU9250 High-Precision 9-axis Gyroscope+Angle 
Works for my use case, your mileage may vary.

# Example useage
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
# df.to_csv(f"{int(time.time())}-imu.csv")


df.to_csv(f"imudata/{filename}.csv")
```
