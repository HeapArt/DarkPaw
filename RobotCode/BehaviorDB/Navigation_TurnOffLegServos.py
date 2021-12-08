import time, math
import random
from .BehaviorDB import BehaviorTemplate

class Navigation_TurnOffLegServos(BehaviorTemplate):
  def __init__(self):
    super().__init__("Navigation", "Turn Off Leg Servos")
    return

  def wake(self, iRobot):
    print("Updated Form")
    wHW = iRobot.getHardware()

    wForm = {}
    
    wForm["All"] = False
    for wi in range(0, wHW.getLegCount()):
      wForm[wHW.getLegName(wi)] = False
    
    self.defineParametersForm(wForm)
    
    return


  def start(self, iRobot):
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    wHW = iRobot.getHardware()
    
    if "All" in self.getParameters():
      wHW.turnOffAllLegs()
    else:
      for wi in range(0, wHW.getLegCount()):
        wName = wHW.getLegName(wi)
        if wName in self.getParameters():
          if True == self.getParameters()[wName]:
            wHW.turnOffLeg(wi)
      
    return True


_Behavior = Navigation_TurnOffLegServos()
