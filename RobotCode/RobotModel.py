import json
from os import wait
import time
import math
import threading

from .HardwareModel import HardwareModel
from .BehaviorModel import BehaviorModel

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
      
    self._hardwware = HardwareModel()
    self._behavior = BehaviorModel()

    self._robotState = eRobotState_VOID
    self._robotThread = None
    return

  def cleanConfig(self):

    if eRobotState_WAKE <= self._robotState:
      self.sleep()

    self._hardwware.cleanConfig()

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

    if "Hardware Setup" in wConfigObj:
      self._hardwware.loadConfig(wConfigObj["Hardware Setup"])

    if "Behavior Setup" in wConfigObj:
      self._behavior.loadConfig(wConfigObj["Behavior Setup"])


    self._robotState = eRobotState_LOAD

    return True


  def wake(self):

    if eRobotState_LOAD > self._robotState:
      return False

    if eRobotState_WAKE <= self._robotState:
      self.sleep()

    print("Robot Waking")

    self._hardwware.wake(self)
    self._behavior.wake(self)

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

    self._hardwware.sleep(self)
    self._behavior.sleep(self)

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
  
    self._hardwware.tick(self, iDt, iElapseTime)
    self._behavior.tick(self, iDt, iElapseTime)

    return

  def getHardware(self):
    return self._hardwware

  def getBehavior(self):
    return self._behavior

_gRobotModel = None
def getRobotModel():
  global _gRobotModel
  if None == _gRobotModel:
    _gRobotModel = RobotModel()
  return _gRobotModel