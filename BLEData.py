class BLEData:

    GRAVITY = 9.8

    def __init__(self, data):

        self.header = data[0]
        self.flag_bit = data[1]
        # Acceleration Data
        self.axL = data[2]
        self.axH = data[3]
        self.ayL = data[4]
        self.ayH = data[5]
        self.azL = data[6]
        self.azH = data[7]
        # Angular Velocity Data
        self.wxL = data[8]
        self.wxH = data[9]
        self.wyL = data[10]
        self.wyH = data[11]
        self.wzL = data[12]
        self.wzH = data[13]
        # Roll Data
        self.rollL = data[14]
        self.rollH = data[15]
        self.pitchL = data[16]
        self.pitchH = data[17]
        self.yawL = data[18]
        self.yawH = data[19]

        self.accelX = ((self.axH << 8) + self.axL) / 32768 * 16
        self.accelY = ((self.ayH << 8) + self.ayL) / 32768 * 16
        self.accelZ = ((self.azH << 8) + self.azL) / 32768 * 16

        self.angleX = ((self.wxH << 8) + self.wxL) / 32768 * 2000
        self.angleY = ((self.wyH << 8) + self.wyL) / 32768 * 2000
        self.angleZ = ((self.wzH << 8) + self.wzL) / 32768 * 2000


    def __str__(self):
        return f"AccelX: {self.accelX} AccelY: {self.accelY} AccelZ: {self.accelZ} \nAngleX: {self.angleX} AngleY: {self.angleY} AngleZ: {self.angleZ}"