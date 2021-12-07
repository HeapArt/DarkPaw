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
    self._mColor = [0,0,0]

    wForm = {}
    wForm["Frequency"] = 0.5
    if "Custom" == iColorName:
      wForm["Color"] = "#FFFFFF"
    if "Rainbow" == iColorName:
      wForm["Color Speed"] = 1.0
    self.defineParametersForm(wForm)

    return

  def start(self, iRobot):

    wColor = [0,0,0]

    if "Red" == self._mColorname:
      wColor = [255,0,0]
    
    elif "Blue" == self._mColorname:
      wColor = [0,0,255]

    elif "Green" == self._mColorname:
      wColor = [0,255,0]

    elif "Custom" == self._mColorname:
      wStrColor = self.getParameters()["Color"]

      wColor = []
      wIndex = []
      for wi in (1, 3, 5):
        wDecimal = int(wStrColor[wi:wi+2], 16)
        wColor.append(wDecimal)

    self._mColor = wColor
    return True


  def stop(self, iRobot):
    return True


  def tick(self, iRobot, iDt, iElapseTime):

    if "Rainbow" == self._mColorname:
      wIndex = 0
      wIncrement = self.getParameters()["Color Speed"]
      if wIncrement < 1:
        wIncrement = 1

      wColorSize = len(self._mColor)
      for wi in range(0, wColorSize):
        if 0 != self._mColor[wi]:
          wIndex = wi
          break
      wFirstIndex = wIndex
      wSecondIndex = (wIndex + 1) % wColorSize
      if 0 == wIndex:
        if 0 != self._mColor[wColorSize - 1]:
          wFirstIndex = wColorSize - 1
          wSecondIndex = 0
      if 255 == self._mColor[wSecondIndex]:
        if 0 < self._mColor[wFirstIndex]:
          self._mColor[wFirstIndex] = self._mColor[wFirstIndex] - wIncrement
      elif 255 == self._mColor[wFirstIndex]:
        if 255 > self._mColor[wSecondIndex]:
          self._mColor[wSecondIndex] = self._mColor[wSecondIndex] + wIncrement
      else:
        if 255 > self._mColor[wFirstIndex]:
          self._mColor[wFirstIndex] = self._mColor[wFirstIndex] + wIncrement

      for wi in range(0, wColorSize):
        if self._mColor[wi] >= 255:
          self._mColor[wi] = 255
        elif self._mColor[wi] <= 0:
          self._mColor[wi] = 0 

    if False:
      print("Color : {}".format(self._mColor))
    wColor = self._mColor
    wHW = iRobot.getHardware()
    
    if self._mLeftEnabled:
      wHW.setLEDWipe_Left()

    if self._mRightEnabled:
      wHW.setLEDWipe_Right()

    wFrequency = self.getParameters()["Frequency"]
      
    wPhaseShift = math.pi/18
    for i in range(0, wHW.getLEDCount_Left()):
      wWave = 0.5*(math.sin(iElapseTime*2*math.pi*wFrequency + i*wPhaseShift)+1)
      if self._mLeftEnabled:
        wHW.setLED_Left(i,int(wWave*wColor[0]),int(wWave*wColor[1]),int(wWave*wColor[2]))
      if self._mRightEnabled:
        wHW.setLED_Right(i,int(wWave*wColor[0]),int(wWave*wColor[1]),int(wWave*wColor[2]))

    return True

_Behavior_l1 = Behavior_BreathingLED("Red", True, False)
_Behavior_l2 = Behavior_BreathingLED("Blue", True, False)
_Behavior_l3 = Behavior_BreathingLED("Green", True, False)
_Behavior_l4 = Behavior_BreathingLED("Custom", True, False)
_Behavior_l5 = Behavior_BreathingLED("Rainbow", True, False)

_Behavior_r1 = Behavior_BreathingLED("Red", False, True)
_Behavior_r2 = Behavior_BreathingLED("Blue", False, True)
_Behavior_r3 = Behavior_BreathingLED("Green", False, True)
_Behavior_r4 = Behavior_BreathingLED("Custom", False, True)
_Behavior_r5 = Behavior_BreathingLED("Rainbow", False, True)
