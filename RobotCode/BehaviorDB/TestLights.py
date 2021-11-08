import time, math
from .BehaviorDB import BehaviorTemplate

class Behavior_TestLights(BehaviorTemplate):
  def __init__(self):
    super().__init__("Light", "TestLights")
    return

  def wake(self, iRobot):
    wHW = iRobot.getHardware()
    wWaitTime = 0.25

    wHW.setLEDWipe_Left(iRed=255)
    wHW.update_LED()
    time.sleep(wWaitTime)
    wHW.setLEDWipe_Left(iGreen=255)
    wHW.update_LED()
    time.sleep(wWaitTime)
    wHW.setLEDWipe_Left(iBlue=255)
    wHW.update_LED()
    time.sleep(wWaitTime)
    wHW.setLEDWipe_Left()
    

    wHW.setLEDWipe_Right(iRed=255)
    wHW.update_LED()
    time.sleep(wWaitTime)
    wHW.setLEDWipe_Right(iGreen=255)
    wHW.update_LED()
    time.sleep(wWaitTime)
    wHW.setLEDWipe_Right(iBlue=255)
    wHW.update_LED()
    time.sleep(wWaitTime)
    wHW.setLEDWipe_Right()
    wHW.update_LED()
    time.sleep(wWaitTime)
    
    for i in range(0, wHW.getLEDCount_Left()):
        wHW.setLEDWipe_Left()
        wHW.setLED_Left(i,255,255,255)
        wHW.update_LED()
        time.sleep(wWaitTime)
    
    for i in range(0, wHW.getLEDCount_Right()):
        wHW.setLEDWipe_Right()
        wHW.setLED_Right(i,255,255,255)
        wHW.update_LED()
        time.sleep(wWaitTime)
    
    wHW.setLEDWipe_Left()
    wHW.setLEDWipe_Right()

    return True


  def sleep(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):
    wHW = iRobot.getHardware()

    for i in range(0, wHW.getLEDCount_Left()):
        wWave = int(0.5*(math.sin(10*iElapseTime/math.pi + i*math.pi/18)+1)*255)
        wHW.setLED_Left(i,iBlue = wWave)
        wHW.setLED_Right(i,iBlue = wWave)
    
    return True

_Behavior = Behavior_TestLights()