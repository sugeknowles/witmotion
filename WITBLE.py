import asyncio
import BLESearcher
from bleak import BleakClient
import binascii
from BLEData import BLEData

DEVICE_NAME = "WT901BLE68"
CHARACTERISTIC_READ = "0000ffe4-0000-1000-8000-00805f9a34fb"
CHARACTERISTIC_WRITE = "0000ffe9-0000-1000-8000-00805f9a34fb"
RATE_BYTES = 0x08 # 50Hz Return Rate

class WITBLE():

    mac_address = None
    client = None


    def __init__(self, mac_address):
        self.mac_address = mac_address


    def process_data(self, data):
        bledata = BLEData(data)
        print(bledata)

    def notification_handler(self, sender, data):        
        if len(data) == 40:
            packet_a = data[:len(data)//2]
            packet_b = data[len(data)//2:]
            self.process_data(packet_a)
            self.process_data(packet_b)
        else:
            self.process_data(data)


    async def connect(self):
        if self.mac_address:
            async with BleakClient(self.mac_address) as client:
                svcs = await client.get_services()
                for service in svcs:
                    print(f"Service: {service}")
                    for characteristic in service.characteristics:
                        print(f"\tCharacteristic: {characteristic}")
                        for property in characteristic.properties:
                            print(f"\t\tProperty: {property}")
                    # descriptors = client.read_gatt_descriptor()

                msg_bytes = bytearray([0xff, 0xaa, 0x03, RATE_BYTES, 0x00]);
                print(f"Sending rate message: {msg_bytes}")
                await client.write_gatt_char(CHARACTERISTIC_WRITE, msg_bytes)                
                self.client = client
        else:
            print("Can't connect. MAC not set.")

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
        else:
            print("Can't disconnect.  Not connected.")

    async def subscribe(self):
        async with self.client:
            await self.client.start_notify(CHARACTERISTIC_READ, self.notification_handler)
            await asyncio.sleep(10000.0)
            await self.client.stop_notify(CHARACTERISTIC_READ)



mac = BLESearcher.search(DEVICE_NAME, 5)
print(f"Connecting to {mac}")
witble = WITBLE(mac)
asyncio.run(witble.connect())
asyncio.run(witble.subscribe())
# asyncio.run(witble.disconnect())