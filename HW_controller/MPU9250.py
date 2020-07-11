from datetime import datetime   # timestamp
import time     #time
import smbus
import math
class MPU9250:
    def __init__(self):
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus=smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.addr= 0x68  # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.addr, self.power_mgmt_1,0)
        self.fout = open('gyro.txt', 'w')
        self.gyro_xout=0
        self.gyro_yout=0
        self.gyro_zout=0
        self.accel_xout = 0
        self.accel_yout =0
        self.accel_zout = 0
#         self.gyro_out=""
#         self.acc_out=""
        self.data=""
        self.roty=0
        self.rotx=0
    
    def read_byte(self,adr):
        return self.bus.read_byte_data(self.addr,adr)
    
    def read_word(self,adr):
        high=self.bus.read_byte_data(self.addr,adr)
        low =self.bus.read_byte_data(self.addr,adr+1)
        val= (high<<8)+low
        return val
        
    def read_word_2c(self,adr):
        val=self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def get_y_rotation(x,y,z):
        radians=math.atan2(x,math.sqrt((y*y)+(z*z)))
        val=-radians*math.pi/180
        return val

    def get_x_rotation(x,y,z):
        radians=math.atan2(y,math.sqrt((x*x)+(z*z)))
        return math.degrees(radians)

    def gyro_out(self):
        self.gyro_xout =self.read_word_2c(0x43)
        self.gyro_yout =self.read_word_2c(0x45)
        self.gyro_zout =self.read_word_2c(0x47)
        self.gyro_xout=self.gyro_xout/131
        self.gyro_yout=self.gyro_yout/131
        self.gyro_zout=self.gyro_zout/131
#         self.gyro_out=str(self.gyro_xout)+","+str(self.gyro_yout)+","+str(self.gyro_zout)

    def accl_out(self):
        self.accel_xout = self.read_word_2c(0x3b)
        self.accel_yout = self.read_word_2c(0x3d)
        self.accel_zout = self.read_word_2c(0x3f)
        self.accel_xout = self.accel_xout / 16384.0
        self.accel_yout = self.accel_yout / 16384.0
        self.accel_zout = self.accel_zout / 16384.0
#         self.acc_out=str(self.accel_xout)+","+str(self.accel_yout)+","+str(self.accel_zout)

    def read(self):
        self.gyro_out()
        self.accl_out()
        self.rotx=self.get_x_rotation(self.accel_xout, self.accel_yout, self.accel_zout)
        self.roty=self.get_y_rotation(self.accel_xout, self.accel_yout, self.accel_zout)
        print("x rotation: ", self.rotx)
        print("y rotation: ", self.roty)
    
    def filewrite(self):
        timestamp=datetime.fromtimestamp(time.time())
        self.data=str(timestamp)+">> "+str(self.rotx)+","+str(self.roty)+","+self.gyroout
        self.fout.write(self.data)

if __name__=="__main__":
    mpu=MPU9250()
    mpu.gyro_out()
    for i in range(1,10000):
        mpu.read()
        mpu.filewrite()
    