import BLESearcher
from WITBLE import WITBLE

import asyncio

mac = BLESearcher.search(WITBLE.DEVICE_NAME, 5)
print(f"Connecting to {mac}")
witble = WITBLE(mac)
asyncio.run(witble.connect(WITBLE.RATE_50HZ))
print("Connected..  Subscribing to data.")
asyncio.run(witble.subscribe(5.0))
print("Subscription complete.")
print(len(witble.data))