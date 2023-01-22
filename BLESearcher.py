import asyncio
import struct

from bleak import BleakScanner

class BLESearcher:

    device_mac = None
    search_name = "NOTSET"
    timeout_seconds = 20

    def __init__(self, timeout_seconds):
        self.timeout_seconds = timeout_seconds
        self._scanner = BleakScanner()
        self._scanner.register_detection_callback(self.detection_callback)
        self.scanning = asyncio.Event()

    def detection_callback(self, device, advertisement_data):
        if device.name == self.search_name:
            print(f"Device named {self.search_name} found. MAC: {device.address}")
            self.device_mac = device.address

    async def run_search(self, search_name, loop):
        self.search_name = search_name
        await self._scanner.start()
        self.scanning.set()
        end_time = loop.time() + self.timeout_seconds
        while self.scanning.is_set():
            if loop.time() > end_time:
                self.scanning.clear()
                print(f"Searching for {self.search_name} timed out.")
            if self.device_mac:
                self.scanning.clear()
            await asyncio.sleep(0.1)
        await self._scanner.stop()

def search(search_name, timeout):
    ble_searcher = BLESearcher(5)
    print(f"Starting scan. {ble_searcher.timeout_seconds} second timeout.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ble_searcher.run_search(search_name, loop))
    print(f"Returned MAC: {ble_searcher.device_mac}")
    return ble_searcher.device_mac

    