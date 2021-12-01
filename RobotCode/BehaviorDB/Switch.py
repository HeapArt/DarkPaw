import time, math
from .BehaviorDB import BehaviorTemplate

class Behavior_Switch(BehaviorTemplate):
  def __init__(self, iId, iState):
    wName = "Turn On"
    if False == iState:
      wName = "Turn Off"
    super().__init__("Switch {}".format(iId), wName)
    self._mSwitchId = iId 
    self._mSwitchState = iState 

    wForm = {}
    wForm["flicker"] = False
    self.defineParametersForm(wForm)
    return

  def start(self, iRobot):
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    wHW = iRobot.getHardware()
    wHW.setSwitch(self._mSwitchId, self._mSwitchState)
    return True


_Behavior_0_on = Behavior_Switch(0, True)
_Behavior_0_off = Behavior_Switch(0, False)
_Behavior_1_on = Behavior_Switch(1, True)
_Behavior_1_off = Behavior_Switch(1, False)