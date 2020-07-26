from datetime import datetime   # timestamp
import time     #time
import smbus
import math

class MPU9250:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        #MPU6050
        # MPU6050 Registers
        self.MPU6050_ADDR = 0x68
        self.PWR_MGMT_1   = 0x6B
        self.CONFIG       = 0x1A
        self.SMPLRT_DIV   = 0x19
        self.GYRO_CONFIG  = 0x1B
        self.ACCEL_CONFIG = 0x1C
        self.INT_ENABLE   = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.TEMP_OUT_H   = 0x41
        self.GYRO_XOUT_H  = 0x43
        self.GYRO_YOUT_H  = 0x45
        self.GYRO_ZOUT_H  = 0x47
        # alter sample rate (stability)
        self.samp_rate_div = 0 # sample rate = 8 kHz/(1+samp_rate_div)
        self.bus.write_byte_data(self.MPU6050_ADDR, self.SMPLRT_DIV, self.samp_rate_div)
        time.sleep(0.1)
        # reset all sensors
        self.bus.write_byte_data(self.MPU6050_ADDR,self.PWR_MGMT_1,0x00)
        time.sleep(0.1)
        # power management and crystal settings
        self.bus.write_byte_data(self.MPU6050_ADDR, self.PWR_MGMT_1, 0x01)
        time.sleep(0.1)
        #Write to Configuration register
        self.bus.write_byte_data(self.MPU6050_ADDR, self.CONFIG, 0)
        time.sleep(0.1)
        #Write to Gyro configuration register
        gyro_config_sel = [0b00000,0b010000,0b10000,0b11000] # byte registers
        gyro_config_vals = [250.0,500.0,1000.0,2000.0] # degrees/sec
        gyro_indx = 0
        self.bus.write_byte_data(self.MPU6050_ADDR, self.GYRO_CONFIG, int(gyro_config_sel[gyro_indx]))
        time.sleep(0.1)
        #Write to Accel configuration register
        accel_config_sel = [0b00000,0b01000,0b10000,0b11000] # byte registers
        accel_config_vals = [2.0,4.0,8.0,16.0] # g (g = 9.81 m/s^2)
        accel_indx = 0                            
        self.bus.write_byte_data(self.MPU6050_ADDR, self.ACCEL_CONFIG, int(accel_config_sel[accel_indx]))
        time.sleep(0.1)
        # interrupt register (related to overflow of data [FIFO])
        self.bus.write_byte_data(self.MPU6050_ADDR, self.INT_ENABLE, 1)
        time.sleep(0.1)
        self.gyro_sens=gyro_config_vals[gyro_indx]
        self.accel_sens=accel_config_vals[accel_indx]
      
        #AK8963
        self.AK8963_ADDR = 0x0C
        self.AK8963_CNTL = 0x0A
        self.AK8963_ST1  = 0x02
        self.HXH         = 0x04
        self.HYH         = 0x06
        self.HZH         = 0x08
        self.AK8963_ST2  = 0x09
        self.mag_sens = 4900.0 
        self.bus.write_byte_data(self.AK8963_ADDR,self.AK8963_CNTL,0x00)
        time.sleep(0.1)
        self.AK8963_bit_res = 0b0001 # 0b0001 = 16-bit
        self.AK8963_samp_rate = 0b0110 # 0b0010 = 8 Hz, 0b0110 = 100 Hz
        self.AK8963_mode = (self.AK8963_bit_res <<4)+self.AK8963_samp_rate # bit conversion
        self.bus.write_byte_data(self.AK8963_ADDR,self.AK8963_CNTL,self.AK8963_mode)
        time.sleep(0.1)
        
        self.fout = open('MPU9250.txt', 'w')
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0

        self.w_x = 0
        self.w_y = 0
        self.w_z = 0

        self.gyro_data=""
        self.accel_data=""
        self.head_data=""
        self.data=""
        
    def read_raw_bits(self,register):
        # read accel and gyro values
        high = self.bus.read_byte_data(self.MPU6050_ADDR, register)
        low = self.bus.read_byte_data(self.MPU6050_ADDR, register+1)
        # combine higha and low for unsigned bit value
        value = ((high << 8) | low)
        # convert to +- value
        if(value > 32768):
            value -= 65536
        return value
    
    def mpu6050_data(self):
        # raw acceleration bits
        acc_x = self.read_raw_bits(self.ACCEL_XOUT_H)
        acc_y = self.read_raw_bits(self.ACCEL_YOUT_H)
        acc_z = self.read_raw_bits(self.ACCEL_ZOUT_H)

        # raw temp bits
        ##    t_val = self.read_raw_bits(self.TEMP_OUT_H) # uncomment to read temp
    
        # raw gyroscope bits
        gyro_x = self.read_raw_bits(self.GYRO_XOUT_H)
        gyro_y = self.read_raw_bits(self.GYRO_YOUT_H)
        gyro_z = self.read_raw_bits(self.GYRO_ZOUT_H)

        #convert to acceleration in g and gyro dps
        self.a_x = (acc_x/(32768.0))*self.accel_sens
        self.a_y = (acc_y/(32768.0))*self.accel_sens
        self.a_z = (acc_z/(32768.0))*self.accel_sens

        self.w_x = (gyro_x/(32768.0))*self.gyro_sens
        self.w_y = (gyro_y/(32768.0))*self.gyro_sens
        self.w_z = (gyro_z/(32768.0))*self.gyro_sens

        ##    self.temp = ((t_val)/333.87)+21.0 # uncomment and add below in return
        self.gyro_data='Gyro: '+str(self.w_x)+","+str(self.w_y )+","+str(self.w_z)
        self.accel_data = 'Accel: '+str(self.a_x )+","+str(self.a_y)+","+str(self.a_z)
        
    def AK8963_reader(self,register):
        # read magnetometer values
        low = self.bus.read_byte_data(self.AK8963_ADDR, register-1)
        high = self.bus.read_byte_data(self.AK8963_ADDR, register)
        # combine higha and low for unsigned bit value
        value = ((high << 8) | low)
        # convert to +- value
        if(value > 32768):
            value -= 65536
        return value

    def AK8963_data(self):
    # raw magnetometer bits

        loop_count = 0
        while 1:
            mag_x = self.AK8963_reader(self.HXH)
            mag_y = self.AK8963_reader(self.HYH)
            mag_z = self.AK8963_reader(self.HZH)

            # the next line is needed for AK8963
            if bin(self.bus.read_byte_data(self.AK8963_ADDR,self.AK8963_ST2))=='0b10000':
                break
        loop_count+=1
        
        #convert to acceleration in g and gyro dps
        self.m_x = (mag_x/(2.0**15.0))*self.mag_sens
        self.m_y = (mag_y/(2.0**15.0))*self.mag_sens
        self.m_z = (mag_z/(2.0**15.0))*self.mag_sens
        self.head_data='Head: '+str(self.m_x )+","+str(self.m_y)+","+str(self.m_z)

    def read(self):
        self.mpu6050_data()
        self.AK8963_data()
        print(self.gyro_data)
        print(self.accel_data)
        print(self.head_data)

    def filewrite(self):
        timestamp=datetime.fromtimestamp(time.time())
        self.data=str(timestamp)+"\n "+self.gyro_data+"\n"+self.accel_data+"\n"+self.head_data+"\n"+"------------------------------\n"
        self.fout.write(self.data)

if __name__=="__main__":
    mpu=MPU9250()
    for i in range(1,10000):
        mpu.read()
        mpu.filewrite()
