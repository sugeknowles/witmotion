import bitstring
import math

class BLEData:

    data = None
    data_raw = None
    packet = None


    def convert_bytes(self, lowbyte, highbyte):
        concat_value = (highbyte << 8) | lowbyte
        bit = bitstring.Bits(uint=concat_value, length=16)
        return bit.unpack('int')[0] / 32768
        

    def get_acc_angles(self, ax, ay, az):
        phi = math.atan2(ay, math.sqrt(ax ** 2.0 + az ** 2.0))
        theta = math.atan2(-ax, math.sqrt(ay ** 2.0 + az ** 2.0))
        return [phi, theta]

    def __init__(self, packet):

        # Header Data
        self.packet = packet
        self.header = packet[0]
        self.flag_bit = packet[1]

        # Acceleration Data
        self.axL = packet[2]
        self.axH = packet[3]
        self.ayL = packet[4]
        self.ayH = packet[5]
        self.azL = packet[6]
        self.azH = packet[7]

        # Angular Velocity Data
        self.wxL = packet[8]
        self.wxH = packet[9]
        self.wyL = packet[10]
        self.wyH = packet[11]
        self.wzL = packet[12]
        self.wzH = packet[13]

        # Roll Data
        self.rollL = packet[14]
        self.rollH = packet[15]
        self.pitchL = packet[16]
        self.pitchH = packet[17]
        self.yawL = packet[18]
        self.yawH = packet[19]

        # Calculate values from bytes
        self.accelX = self.convert_bytes(self.axL, self.axH) * 16
        self.accelY = self.convert_bytes(self.ayL, self.ayH) * 16
        self.accelZ = self.convert_bytes(self.azL, self.azH) * 16

        self.angleX = self.convert_bytes(self.wxL, self.wxH) * 2000
        self.angleY = self.convert_bytes(self.wyL, self.wyH) * 2000
        self.angleZ = self.convert_bytes(self.wzL, self.wzH) * 2000

        self.roll = self.convert_bytes(self.rollL, self.rollH) * 180
        self.pitch = self.convert_bytes(self.pitchL, self.pitchH) * 180
        self.yaw = self.convert_bytes(self.yawL, self.yawH) * 180

        angles = self.get_acc_angles(self.accelX, self.accelY, self.accelZ)
        self.phi = angles[0]
        self.theta = angles[1]

        self.data = [self.accelX, self.accelY, self.accelZ, self.angleX, self.angleY, self.angleZ, self.roll, self.pitch, self.yaw, self.phi, self.theta]
        # self.data = [self.axL, self.axH, self.ayL, self.ayH, self.azL, self.azH]
    def __str__(self):
        return f"AccelX: {self.accelX} AccelY: {self.accelY} AccelZ: {self.accelZ} \nAngleX: {self.angleX} AngleY: {self.angleY} AngleZ: {self.angleZ} \nRoll: {self.roll} Pitch: {self.pitch} Yaw: {self.yaw} Phi: {self.phi} Theta: {self.theta}"