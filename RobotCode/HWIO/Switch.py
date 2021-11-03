import RPi.GPIO as GPIO
import time

class Switch():
    def __init__(self, iGPIO_Pins = []):
        self._gpioMap = []
        for wPin in iGPIO_Pins:
            if wPin > 0 and wPin < 40:
                self._gpioMap.append(int(wPin))

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        for wPin in self._gpioMap:
            GPIO.setup(wPin, GPIO.OUT)
        return

    def switch(self, iIndex, iOn = False):
        if iIndex >= 0:
            if iOn:
                GPIO.output(self._gpioMap[iIndex % len(self._gpioMap)], GPIO.HIGH)
            else:
                GPIO.output(self._gpioMap[iIndex % len(self._gpioMap)], GPIO.LOW)
        return                

    def set_all_switch(self,iOn = False):
        if iOn:
            for wPin in self._gpioMap:
                GPIO.output(wPin, GPIO.HIGH)
        else:
            for wPin in self._gpioMap:
                GPIO.output(wPin, GPIO.LOW)
        return

if __name__ == '__main__':
    wSwitch = Switch([5,6,13])
    try:
        while 1:
            wSwitch.set_all_switch(True)
            print("Light on....")
            time.sleep(1)
            wSwitch.set_all_switch(False)
            print("Light off....")
            time.sleep(1)
    except:
        wSwitch.set_all_switch(False)
    