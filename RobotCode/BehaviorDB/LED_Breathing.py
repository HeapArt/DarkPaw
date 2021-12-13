import time, math
from .BehaviorDB import BehaviorTemplate

class LED_Breathing(BehaviorTemplate):
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
      wColorSpeed = self.getParameters()["Color Speed"]
      if wColorSpeed < 0.01:
        wColorSpeed = 0.01

      wSpaceWidth = 6*255
      wOffset = 2*255

      #initialize to 1 minute to go though all colors
      wPosition = int(wColorSpeed*wSpaceWidth*iElapseTime/60)

      # R : /--\__|/--\__
      # G : __/--\|__/--\
      # B : -\__/-|-\__/-

      for wi in range(0, len(self._mColor)):
        wColorValue = 0
        wChannelPosition = (wPosition + wSpaceWidth - wi*wOffset)%wSpaceWidth
        if wChannelPosition < 255:
          wColorValue = wChannelPosition
        elif wChannelPosition < 3*255:
          wColorValue = 255
        elif wChannelPosition < 4*255:
          wColorValue = 255 - (wChannelPosition - 3*255)
        
        self._mColor[wi] = wColorValue

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


def behaviorCreation(iRobot):
  if 0 != iRobot.getHardware().getLEDCount_Left():
    _Behavior_l1 = LED_Breathing("Red", True, False)
    _Behavior_l2 = LED_Breathing("Blue", True, False)
    _Behavior_l3 = LED_Breathing("Green", True, False)
    _Behavior_l4 = LED_Breathing("Custom", True, False)
    _Behavior_l5 = LED_Breathing("Rainbow", True, False)

  if 0 != iRobot.getHardware().getLEDCount_Right():
    _Behavior_r1 = LED_Breathing("Red", False, True)
    _Behavior_r2 = LED_Breathing("Blue", False, True)
    _Behavior_r3 = LED_Breathing("Green", False, True)
    _Behavior_r4 = LED_Breathing("Custom", False, True)
    _Behavior_r5 = LED_Breathing("Rainbow", False, True)
