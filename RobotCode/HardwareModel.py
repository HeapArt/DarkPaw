import json
from os import wait
import time
import math
import threading

from .HWIO.LEDController import LEDController
from .HWIO.SwitchController import SwitchController


eRobotState_VOID = 0
eRobotState_LOAD = 1
eRobotState_WAKE = 2
eRobotState_RUN = 3
eRobotState_DROWZEE = 4
eRobotState_SLEEP = 5

class HardwareModel:
  def __init__(self):
    
    self._led_left = []
    self._led_right = []
    self._led_Controller = None

    self._switch_state = []
    self._switch_Controller = None

    self._legs = []
    self._servo_controller = None
    return

  def cleanConfig(self):
    
    self._led_left = []
    self._led_right = []
    
    if None != self._led_Controller:
      del self._led_Controller
      self._led_Controller = None

    self._switch_state = []

    if None != self._switch_Controller:
      del self._switch_Controller
      self._switch_Controller = None

    return


  def loadConfig(self, iConfigObject):

    # Extract LED Mapping
    if "LED" in iConfigObject:
      self._led_Controller = LEDController()
      wLedConf = iConfigObject["LED"]
      if "left" in wLedConf:
        for wIndex in wLedConf["left"]:
          wI = int(wIndex)
          if wI >= 0:
            self._led_left.append([wI,0,0,0]) 
      
      if "right" in wLedConf:
        for wIndex in wLedConf["right"]:
          wI = int(wIndex)
          if wI >= 0:
            self._led_right.append([wI,0,0,0]) 
    
    # Extract Switch Mapping
    if "Switch GPIO" in iConfigObject:
      wPinArray = []
      self._switch_state = []
      for wPin in iConfigObject["Switch GPIO"]:
        if wPin > 0:
          wPinArray.append(int(wPin))
          self._switch_state.append(False)

      self._switch_Controller = SwitchController(wPinArray)
      
    return True


  def wake(self, iRobot):

    return True


  def sleep(self, iRobot):

    self.setLEDWipe_Left(0,0,0)
    self.setLEDWipe_Right(0,0,0)
    self.update_LED()

    self.setSwitchAll(False)
    self.update_Switchs()

    return


  def tick(self, iRobot, iDt, iElapseTime):
  
    self.update_LED()
    self.update_Switchs()
    return


  def update_LED(self):
    if None != self._led_Controller:
      self._led_Controller.setColorSet(self._led_left)
      self._led_Controller.setColorSet(self._led_right)
    return


  def update_Switchs(self):
    if None != self._switch_Controller:
      for wi in range(0, len(self._switch_state)):
        self._switch_Controller.switch(wi, self._switch_state[wi])
    return


  def setLED_Left(self, iIndex, iRed = 0, iGreen = 0, iBlue = 0):
    if iIndex >= 0:
      if iIndex < len(self._led_left):
        wPixel = self._led_left[iIndex]
        wPixel[1] = iRed
        wPixel[2] = iGreen
        wPixel[3] = iBlue
        return True
    return False


  def setLEDWipe_Left(self, iRed = 0, iGreen = 0, iBlue = 0):
    for wPixel in self._led_left:
      wPixel[1] = iRed
      wPixel[2] = iGreen
      wPixel[3] = iBlue
    return True


  def setLED_Right(self, iIndex, iRed = 0, iGreen = 0, iBlue = 0):
    if iIndex >= 0:
      if iIndex < len(self._led_right):
        wPixel = self._led_right[iIndex]
        wPixel[1] = iRed
        wPixel[2] = iGreen
        wPixel[3] = iBlue
        return True
    return False


  def setLEDWipe_Right(self, iRed = 0, iGreen = 0, iBlue = 0):
    for wPixel in self._led_right:
      wPixel[1] = iRed
      wPixel[2] = iGreen
      wPixel[3] = iBlue
    return True

  
  def getLEDCount_Left(self):
    return len(self._led_left)


  def getLEDColor_Left(self):
    if iIndex >= 0:
      if iIndex < len(self._led_left):
        wPixel = self._led_left[iIndex]
        return (wPixel[1],wPixel[2],wPixel[3])
    return None


  def getLEDCount_Right(self):
      return len(self._led_right)


  def getLEDColor_Right(self):
    if iIndex >= 0:
      if iIndex < len(self._led_right):
        wPixel = self._led_right[iIndex]
        return (wPixel[1],wPixel[2],wPixel[3])
    return None


  def setSwitch(self, iIndex, iOn = False):
    if iIndex >= 0:
      if iIndex < len(self._switch_state):
        self._switch_state[iIndex] = iOn
    return
  
  def setSwitchAll(self, iOn = False):
    for wSwitch in self._switch_state:
      wSwitch = iOn
    return


  def getSwitchCount(self):
      return len(self._switch_state)


  def getLEDColor_Right(self):
    if iIndex >= 0:
      if iIndex < len(self._switch_state):
        return self._switch_state[iIndex]
    return None
