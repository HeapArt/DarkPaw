import time, math
from .BehaviorDB import BehaviorTemplate

class Behavior_TestLED(BehaviorTemplate):
  def __init__(self):
    super().__init__("LED", "Test LED")
    self._mState = 0
    self._mStateWaitElaspTime = 0.0
    return

  def start(self, iRobot):
    self._mState = 0
    self._mStateWaitElaspTime = 0.0
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    wHW = iRobot.getHardware()
    wWaitTime = 1.0

    if 0 == self._mState:
      pass

    if 1 == self._mState:
      wHW.setLEDWipe_Left(iRed=255)

    if 2 == self._mState:
      wHW.setLEDWipe_Left(iBlue=255)

    if 3 == self._mState:
      wHW.setLEDWipe_Left(iGreen=255)

    if 4 == self._mState:
      wHW.setLEDWipe_Left()

    if 5 == self._mState:
      wHW.setLEDWipe_Right(iRed=255)

    if 6 == self._mState:
      wHW.setLEDWipe_Right(iBlue=255)

    if 7 == self._mState:
      wHW.setLEDWipe_Right(iGreen=255)

    if 8 == self._mState:
      wHW.setLEDWipe_Right()

    wBaseStateValue = 9
    if wBaseStateValue <= self._mState:
      if wHW.getLEDCount_Left() + wBaseStateValue > self._mState:
        wLEDId = self._mState - wBaseStateValue
        wHW.setLEDWipe_Left()
        wHW.setLED_Left(wLEDId,255,255,255)


    wBaseStateValue = wBaseStateValue + wHW.getLEDCount_Left() 
    if wBaseStateValue <= self._mState:
      if wHW.getLEDCount_Right() + wBaseStateValue > self._mState:
        wLEDId = self._mState - wBaseStateValue
        wHW.setLEDWipe_Right()
        wHW.setLED_Right(wLEDId,255,255,255)

    wBaseStateValue = wBaseStateValue + wHW.getLEDCount_Right() 
    if wBaseStateValue < self._mState:
      for i in range(0, wHW.getLEDCount_Left()):
        wWave = int(0.5*(math.sin(10*iElapseTime/math.pi + i*math.pi/18)+1)*255)
        wHW.setLED_Left(i,iBlue = wWave)
        wHW.setLED_Right(i,iBlue = wWave)
    
    self.stateWaitTimer(wWaitTime, iDt)

    return True


  def stateWaitTimer(self , iWaitTime, iDt):
    self._mStateWaitElaspTime = self._mStateWaitElaspTime + iDt
    if self._mStateWaitElaspTime > iWaitTime:
      self._mState = self._mState + 1
      self._mStateWaitElaspTime = 0.0


_Behavior = Behavior_TestLED()