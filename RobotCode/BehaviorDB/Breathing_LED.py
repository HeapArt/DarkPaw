import time, math
from .BehaviorDB import BehaviorTemplate

class Behavior_BreathingLED(BehaviorTemplate):
  def __init__(self, iColorName, iLeft = False, iRight = False):
    
    self._mLeftEnabled = False
    self._mRightEnabled = False
    wType = "LED"
    wName = "Breathing {}".format(iColorName)
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

    self._mColorname = iColorName

    wForm = {}
    wForm["Frequency"] = 0.5
    self.defineParametersForm(wForm)

    return

  def start(self, iRobot):
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    wColor = [0,0,0]

    if "Red" == self._mColorname:
      wColor = [1,0,0]
    
    if "Blue" == self._mColorname:
      wColor = [0,0,1]

    if "Green" == self._mColorname:
      wColor = [0,1,0]

    wHW = iRobot.getHardware()
    
    if self._mLeftEnabled:
      wHW.setLEDWipe_Left()

    if self._mRightEnabled:
      wHW.setLEDWipe_Right()

    wFrequency = self.getParameters()["Frequency"]
    if wFrequency <= 0.0:
      wFrequency = 1.0

    wPeriod = 2*math.pi/ wFrequency
    wPhaseShift = 0.1*wPeriod

    for i in range(0, wHW.getLEDCount_Left()):
      wWave = int(0.5*(math.sin(iElapseTime/wFrequency + i*wPhaseShift)+1)*255)
      if self._mLeftEnabled:
        wHW.setLED_Left(i,wWave*wColor[0],wWave*wColor[1],wWave*wColor[2])
      if self._mRightEnabled:
        wHW.setLED_Right(i,wWave*wColor[0],wWave*wColor[1],wWave*wColor[2])

    return True

_Behavior_l1 = Behavior_BreathingLED("Red", True, False)
_Behavior_l2 = Behavior_BreathingLED("Blue", True, False)
_Behavior_l3 = Behavior_BreathingLED("Green", True, False)

_Behavior_r1 = Behavior_BreathingLED("Red", False, True)
_Behavior_r2 = Behavior_BreathingLED("Blue", False, True)
_Behavior_r3 = Behavior_BreathingLED("Green", False, True)