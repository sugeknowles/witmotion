import asyncio
import BLESearcher
from bleak import BleakClient
import binascii
from BLEData import BLEData
import sys



class WITBLE():

    DEVICE_NAME = "WT901BLE68"
    CHARACTERISTIC_READ = "0000ffe4-0000-1000-8000-00805f9a34fb"
    CHARACTERISTIC_WRITE = "0000ffe9-0000-1000-8000-00805f9a34fb"

    # Return rate constants
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


    mac_address = None
    client = None
    data = []


    def __init__(self, mac_address):
        self.mac_address = mac_address

    def chunker(self, seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def process_data(self, data):
        for packet in self.chunker(data, 20):
            witble_data = BLEData(packet)
            self.data.append(witble_data.data)

    def notification_handler(self, sender, data):        
        # if len(data) > 20:
        #     packet_a = data[:len(data)//2]
        #     packet_b = data[len(data)//2:]
        #     self.process_data(packet_a)
        #     self.process_data(packet_b)
        # else:
        #     self.process_data(data)
        self.process_data(data)

    async def connect(self, rate):
        if self.mac_address:
            async with BleakClient(self.mac_address) as client:                
                rate_message = bytearray([0xff, 0xaa, 0x03, rate, 0x00]);
                await client.write_gatt_char(self.CHARACTERISTIC_WRITE, rate_message)                
                self.client = client
        else:
            print("Can't connect. MAC not set.")

    
    async def calibrate(self):
        # FF AA 01 01 00
        if self.client:
            async with self.client:
                rate_message = bytearray([0xff, 0xaa, 0x01, 0x01, 0x00]);
                await self.client.write_gatt_char(self.CHARACTERISTIC_WRITE, rate_message)                



    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
        else:
            print("Can't disconnect.  Not connected.")


    async def subscribe(self, subscription_time):
        if self.client:
            async with self.client:
                await self.client.start_notify(self.CHARACTERISTIC_READ, self.notification_handler)
                await asyncio.sleep(subscription_time)
                await self.client.stop_notify(self.CHARACTERISTIC_READ)
        else:
            print("Can't subscribe.  Not connected.")