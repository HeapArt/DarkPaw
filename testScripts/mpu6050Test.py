#!usr/bin/python3

from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)
def mpu6050test():
  x = 0
  y = 0
  z = 0

  wx = 0
  wy = 0
  wz = 0

  temperature = 0

  for i in range(0,10):
    accel, gyro, temp = sensor.get_all_data()
    x = x + accel['x']
    y = y + accel['y']
    z = z + accel['z']
    
    wx = wx + gyro['x']
    wy = wy + gyro['y']
    wz = wz + gyro['z']
    
    temperature = temp + temperature

  x = round(x/10 , 2)
  y = round(y/10 , 2)
  z = round(z/10 , 2)

  wx = round(wx/10 , 2)
  wy = round(wy/10 , 2)
  wz = round(wz/10 , 2)

  temperature = round(temperature/10 , 2)

  print('X={}, Y={}, Z={}, WX={}, WY={}, WZ={}, temp={}'.format(x,y,z, wx,wy,wz,temperature))
  time.sleep(0.3)

if __name__ == "__main__":
  try:
    while True:
      mpu6050test()
  except:
    pass