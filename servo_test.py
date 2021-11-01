
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

while 1:
    wInput = input("Enter Servo No and Position : ")
    wInputArr = wInput.split()
    pwm.set_pwm(int(wInputArr[0]), 0, int(wInputArr[1]))
    time.sleep(3)