import time, math
from .BehaviorDB import BehaviorTemplate

class Behavior_TestLED(BehaviorTemplate):
  def __init__(self, iLeft, iRight):
    
    self._mLeftEnabled = False
    self._mRightEnabled = False
    wType = "LED"
    wName = "Test Lights"
    if iLeft != iRight:
      if iLeft:
        wType = wType + " Left"
        self._mLeftEnabled = True
      elif iRight:
        wType = wType + " Right"
        self._mRightEnabled = True
    else:
      self._mLeftEnabled = True
      self._mRightEnabled = True

    super().__init__(wType, wName)
    
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
    wWaitTime = 0.5


    iColorSet = [[255, 0, 0],[0, 255, 0],[0, 0, 255]]

    if self._mState < len(iColorSet):
      wR = iColorSet[self._mState][0]
      wG = iColorSet[self._mState][1]
      wB = iColorSet[self._mState][2]
      if self._mLeftEnabled:
        wHW.setLEDWipe_Left(wR, wG, wB)
      if self._mRightEnabled:
        wHW.setLEDWipe_Right(wR, wG, wB)

    else:
      wBaseStateValue = len(iColorSet)
      if self._mLeftEnabled:
        if wHW.getLEDCount_Left() + wBaseStateValue > self._mState:
          wLEDId = self._mState - wBaseStateValue
          wHW.setLEDWipe_Left()
          wHW.setLED_Left(wLEDId,255,255,255)
      
      if self._mRightEnabled:
        if wHW.getLEDCount_Right() + wBaseStateValue > self._mState:
          wLEDId = self._mState - wBaseStateValue
          wHW.setLEDWipe_Right()
          wHW.setLED_Right(wLEDId,255,255,255)

    wLedCount = wHW.getLEDCount_Left()
    if self._mLeftEnabled == self._mRightEnabled:
      if wLedCount < wHW.getLEDCount_Right():
        wLedCount = wHW.getLEDCount_Right()

    elif self._mRightEnabled:
      wLedCount = wHW.getLEDCount_Right()

    if wLedCount + len(iColorSet) <= self._mState:
      self._mState = 0

    self.stateWaitTimer(wWaitTime, iDt)

    return True


  def stateWaitTimer(self , iWaitTime, iDt):
    self._mStateWaitElaspTime = self._mStateWaitElaspTime + iDt
    if self._mStateWaitElaspTime > iWaitTime:
      self._mState = self._mState + 1
      self._mStateWaitElaspTime = 0.0


_Behavior_l = Behavior_TestLED(True, False)
_Behavior_r = Behavior_TestLED(False, True)