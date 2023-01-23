import BLESearcher
from WITBLE import WITBLE


import asyncio
import pandas as pd
import time


CONNECTION_TIMEOUT = 10

mac = BLESearcher.search(WITBLE.DEVICE_NAME, CONNECTION_TIMEOUT)
print(f"Connecting to {mac}")
witble = WITBLE(mac)
asyncio.run(witble.connect(WITBLE.RATE_200HZ))
print("Calibrating sensor.")
asyncio.run(witble.calibrate())
print("Connected..  Subscribing to data.")
asyncio.run(witble.subscribe(30))
print("Subscription complete.")
print(len(witble.data))
df = pd.DataFrame(witble.data)
df.to_csv(f"{int(time.time())}-imu.csv")