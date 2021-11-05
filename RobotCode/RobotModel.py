import json
from os import wait
import time
import math
import threading

from .HWIO.LED import LED
from .HWIO.Switch import Switch


eRobotState_VOID = 0
eRobotState_LOAD = 1
eRobotState_WAKE = 2
eRobotState_RUN = 3
eRobotState_DROWZEE = 4
eRobotState_SLEEP = 5

class RobotModel:
  def __init__(self):
    
    self._frequency = 25
    self._elaspTime = 0.0
      
    self._led_left = []
    self._led_right = []
    self._led_Controller = None

    self._switch_state = []
    self._switch_Controller = None

    self._robotState = eRobotState_VOID
    self._robotThread = None
    return

  def cleanConfig(self):

    if eRobotState_WAKE <= self._robotState:
      self.sleep()
    
    self._led_left = []
    self._led_right = []
    
    if None != self._led_Controller:
      del self._led_Controller
      self._led_Controller = None

    self._switch_state = []

    if None != self._switch_Controller:
      del self._switch_Controller
      self._switch_Controller = None

    self._robotState = eRobotState_VOID
    return


  def loadConfig(self, iConfigJsonFilePath):
    wConfigObj = None
    try:
      with open(iConfigJsonFilePath, "r") as wConfigFile:
        wConfigObj = json.load(wConfigFile)
    except Exception as e:
      print("Robot Configuration Parsing Error [{}]".format(iConfigJsonFilePath))
      if None != e:
        print(e)
      return False

    if eRobotState_LOAD <= self._robotState:
      self.cleanConfig()

    # Extract Robot Frequency
    if "Operating Frequency Hz" in wConfigObj:
      wFrequency = int (wConfigObj["Operating Frequency Hz"])
      if wFrequency < 1:
        wFrequency = 1
      self._frequency = wFrequency

    # Extract LED Mapping
    if "LED" in wConfigObj:
      self._led_Controller = LED()
      wLedConf = wConfigObj["LED"]
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
    if "Switch GPIO" in wConfigObj:
      wPinArray = []
      self._switch_state = []
      for wPin in wConfigObj["Switch GPIO"]:
        if wPin > 0:
          wPinArray.append(int(wPin))
          self._switch_state.append(False)

      self._switch_Controller = Switch(wPinArray)
      

    self._robotState = eRobotState_LOAD

    return True


  def setBehaviorManager(self, iBehaviorModule = None):
    self._BehaviorModule = iBehaviorModule
    return


  def wake(self):

    if eRobotState_LOAD > self._robotState:
      return False

    if eRobotState_WAKE <= self._robotState:
      self.sleep()

    print("Robot Waking")

    if None != self._BehaviorModule:
      self._BehaviorModule.wake(self)

    self._robotState = eRobotState_WAKE

    self._robotThread = threading.Thread(target=self._run)
    self._robotThread.daemon = True
    self._robotThread.start()

    return True


  def sleep(self):

    if eRobotState_RUN == self._robotState:
      self._robotState = eRobotState_DROWZEE
      if None != self._robotThread:
        self._robotThread.join()
        self._robotThread = None

    
    if None != self._BehaviorModule:
      self._BehaviorModule.sleep(self)

    self.setLEDWipe_Left(0,0,0)
    self.setLEDWipe_Right(0,0,0)
    self.update_LED()

    self.setSwitchAll(False)
    self.update_Switchs()

    wLastState = self._robotState
    self._robotState = eRobotState_SLEEP

    if eRobotState_RUN == wLastState:
      if None != self._robotThread:
        self._robotThread.join()

    self._robotState = eRobotState_SLEEP

    print("Robot Sleeping")
    return


  def _run(self):

    if eRobotState_WAKE != self._robotState:
      return

    print("Robot Running")

    self._robotState = eRobotState_RUN

    if self._frequency < 1:
      self._frequency = 1

    wTimeStep = 1/self._frequency

    wLastDt0 = time.time() - wTimeStep
    while eRobotState_RUN == self._robotState:    
      wt0 = time.time()
      wDt = wt0 - wLastDt0
      wLastDt0 = wt0

      self._elaspTime = self._elaspTime + wDt
      self._tick(wDt, self._elaspTime)

      wt1 = time.time()
      wProcDt = wt1 - wt0
      wSlpT = wTimeStep - wProcDt
      if wSlpT > 0:
        time.sleep(wSlpT)
    
    print("Robot Drowzee")

    return


  def _tick(self, iDt, iElapseTime):

    if None != self._BehaviorModule:
      self._BehaviorModule.tick(self, iDt, iElapseTime)
  
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
    if iIndex > 0:
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
