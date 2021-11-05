import time, math

from RobotCode.BehaviorModel import BehaviorTemplate

class Behavior_TestLights(BehaviorTemplate):
  def __init__(self):
    super().__init__("Light", "TestLights")
    return

  def wake(self, iRobot):
    wWaitTime = 0.25

    iRobot.setLEDWipe_Left(iRed=255)
    iRobot.update_LED()
    time.sleep(wWaitTime)
    iRobot.setLEDWipe_Left(iGreen=255)
    iRobot.update_LED()
    time.sleep(wWaitTime)
    iRobot.setLEDWipe_Left(iBlue=255)
    iRobot.update_LED()
    time.sleep(wWaitTime)
    iRobot.setLEDWipe_Left()
    

    iRobot.setLEDWipe_Right(iRed=255)
    iRobot.update_LED()
    time.sleep(wWaitTime)
    iRobot.setLEDWipe_Right(iGreen=255)
    iRobot.update_LED()
    time.sleep(wWaitTime)
    iRobot.setLEDWipe_Right(iBlue=255)
    iRobot.update_LED()
    time.sleep(wWaitTime)
    iRobot.setLEDWipe_Right()
    iRobot.update_LED()
    time.sleep(wWaitTime)
    
    for i in range(0, iRobot.getLEDCount_Left()):
        iRobot.setLEDWipe_Left()
        iRobot.setLED_Left(i,255,255,255)
        iRobot.update_LED()
        time.sleep(wWaitTime)
    
    for i in range(0, iRobot.getLEDCount_Right()):
        iRobot.setLEDWipe_Right()
        iRobot.setLED_Right(i,255,255,255)
        iRobot.update_LED()
        time.sleep(wWaitTime)
    
    iRobot.setLEDWipe_Left()
    iRobot.setLEDWipe_Right()

    return True


  def sleep(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    for i in range(0, len(iRobot._led_left)):
        wWave = int(0.5*(math.sin(10*iElapseTime/math.pi + i*math.pi/18)+1)*255)
        iRobot.setLED_Left(i,iBlue = wWave)
        iRobot.setLED_Right(i,iBlue = wWave)
    
    return True

_Behavior = Behavior_TestLights()