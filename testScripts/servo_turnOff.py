
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm.set_all_pwm(0,0)