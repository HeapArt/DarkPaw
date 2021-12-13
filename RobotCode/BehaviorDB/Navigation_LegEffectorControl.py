from .BehaviorDB import BehaviorTemplate

class Navigation_LegEffectorControl(BehaviorTemplate):
  def __init__(self):
    super().__init__("Navigation", "Leg Effector Control")
    return

  def wake(self, iRobot):
    wHW = iRobot.getHardware()

    wForm = {}
    
    for wi in range(0, wHW.getLegCount()):
      wForm[wHW.getLegName(wi)] = False
      
    wForm["X (mm)"] = 0.0
    wForm["Y (mm)"] = 0.0
    wForm["Z (mm)"] = 0.0
    
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
          wHW.setLegEffectorPosition(wi, wParameters["X (mm)"], wParameters["Y (mm)"], wParameters["Z (mm)"])
      
    return True


def behaviorCreation(iRobot):
  if 0 != iRobot.getHardware().getLegCount():
    _Behavior = Navigation_LegEffectorControl()
