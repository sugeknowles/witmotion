import witble.BLESearcher as searcher
from witble.WITBLE import WITBLE


import asyncio
import pandas as pd


CONNECTION_TIMEOUT = 10

mac = searcher.search(WITBLE.DEVICE_NAME, CONNECTION_TIMEOUT)
print(f"Connecting to {mac}")
witble = WITBLE(mac)
asyncio.run(witble.connect(WITBLE.RATE_200HZ))
print("Calibrating sensor.")
asyncio.run(witble.calibrate())
print("Connected..  Subscribing to data.")
asyncio.run(witble.subscribe(10, True))
print("Subscription complete.")
print(len(witble.data))
asyncio.run(witble.disconnect())
df = pd.DataFrame(witble.data)
# df.to_csv(f"{int(time.time())}-imu.csv")

filename = "foo"

df.to_csv(f"../puttertrack/imudata/{filename}.csv")