import time, math
import random
from .BehaviorDB import BehaviorTemplate

class Switch_TurnOn(BehaviorTemplate):
  def __init__(self, iId, iState):
    wName = "Turn On"
    if False == iState:
      wName = "Turn Off"
    super().__init__("Switch {}".format(iId), wName)
    self._mSwitchId = iId 
    self._mSwitchState = iState 
    self._mFlickerTimer = 0
    self._mFlickerMode = 0

    wForm = {}
    wForm["Flicker"] = False
    self.defineParametersForm(wForm)
    return

  def start(self, iRobot):

    self._mFlickerMode = 0
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    wHW = iRobot.getHardware()
    wHW.setSwitch(self._mSwitchId, self._mSwitchState)

    if True == self.getParameters()["Flicker"]:

      self._mFlickerTimer = self._mFlickerTimer - iDt
      if 0 == self._mFlickerMode:
        if 0 >= self._mFlickerTimer:
          self._mFlickerTimer = random.random()*0.1
          self._mFlickerMode = 1
      elif 1 == self._mFlickerMode:
        wHW.setSwitch(self._mSwitchId, not self._mSwitchState)
        if 0 >= self._mFlickerTimer:
          self._mFlickerTimer = random.random()*0.1
          self._mFlickerMode = 2
      elif 2 == self._mFlickerMode:
        if 0 >= self._mFlickerTimer:
          self._mFlickerTimer = random.random()*0.25
          self._mFlickerMode = 3
      elif 3 == self._mFlickerMode:
        wHW.setSwitch(self._mSwitchId, not self._mSwitchState)
        if 0 >= self._mFlickerTimer:
          self._mFlickerTimer = random.random()*10
          self._mFlickerMode = 0
      
    return True


_Behavior_0_on = Switch_TurnOn(0, True)
_Behavior_0_off = Switch_TurnOn(0, False)
_Behavior_1_on = Switch_TurnOn(1, True)
_Behavior_1_off = Switch_TurnOn(1, False)