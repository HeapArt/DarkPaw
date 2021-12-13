from .BehaviorDB import BehaviorTemplate

class Navigation_LegServoControl(BehaviorTemplate):
  def __init__(self):
    super().__init__("Navigation", "Leg Servo Control")
    return

  def wake(self, iRobot):
    wHW = iRobot.getHardware()

    wForm = {}
    
    wHighestServoCount = 0
    for wi in range(0, wHW.getLegCount()):
      wForm[wHW.getLegName(wi)] = False
      wServoCount = wHW.getLegServoCount(wi)
      if wServoCount >= wHighestServoCount:
        wHighestServoCount = wServoCount
    
    for wi in range(0, wHighestServoCount):
      wForm["Servo {} (deg)".format(wi)] = 0.0
    
    self.defineParametersForm(wForm)
    
    return


  def start(self, iRobot):
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    wHW = iRobot.getHardware()
    wParameters = self.getParameters()
    for wi in range(0, wHW.getLegCount()):
      wName = wHW.getLegName(wi)
      if wName in wParameters:
        if True == wParameters[wName]:
          for wj in range(0, wHW.getLegServoCount(wi)):
            wHW.setLegServoAngle(wi, wj, wParameters["Servo {} (deg)".format(wj)])
      
    return True

def behaviorCreation(iRobot):
  if 0 != iRobot.getHardware().getLegCount():
    _Behavior = Navigation_LegServoControl()
