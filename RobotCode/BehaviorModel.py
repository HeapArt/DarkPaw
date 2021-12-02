import time
import math
import copy
from .BehaviorDB import getBehaviorDB

class BehaviorModel():
  def __init__(self):
    self._currentBehaviorSet = {}
    self._stopBehaviorSet = {}
    self._startBehaviorSet = {}
    return


  def loadConfig(self, iConfigObject):

    # Setup Initial Behavior
    if "Initial Behavior" in iConfigObject:
      wInitialSetup = iConfigObject["Initial Behavior"]
      for wBehavior in wInitialSetup:
        if "Type" not in wBehavior or "Name" not in wBehavior:
          print("Error parsing Initial Behavior : {}".format(json.dumps(wBehavior)))
          return False

        wParameter = {}
        if "Parameter" in wBehavior:
          wParameter = wBehavior["Parameter"]          
        
        self.selectBehavior(wBehavior["Type"], wBehavior["Name"], wParameter)

    return True


  def getCurrentBahaviorSet(self):
    return copy.deepcopy(self._currentBehaviorSet)


  def selectBehavior(self, iBehaviorType, iBehaviorName, iParameters = {}):
    wBehavior = getBehaviorDB().getBehavior(iBehaviorType, iBehaviorName)
    if None != wBehavior:
      wBehavior.setParameters(iParameters)
      self._startBehaviorSet[iBehaviorType] = [iBehaviorName]
      return True

    return False


  def stopBehavior(self, iBehaviorType, iBehaviorName):
    wBehavior = getBehaviorDB().getBehavior(iBehaviorType, iBehaviorName)
    if None != wBehavior:
      self._stopBehaviorSet[iBehaviorType] = [iBehaviorName]
      return True
    return False


  def wake(self, iRobot):
    if None == iRobot:
      return
    return


  def sleep(self, iRobot):
    if None == iRobot:
      return
    return
  
  
  def tick(self, iRobot, iDt, iElapseTime):
    if None == iRobot:
      return

    for wType in self._stopBehaviorSet:
      wList = self._stopBehaviorSet[wType]
      for wBehaviorName in wList:
        if wType in self._startBehaviorSet:
          if wBehaviorName in self._startBehaviorSet[wType]:
            self._startBehaviorSet[wType].remove(wBehaviorName)
        
        if wType in self._currentBehaviorSet:
          if wBehaviorName in self._currentBehaviorSet[wType]:
            wBehavior = getBehaviorDB().getBehavior(wType, wBehaviorName)
            print("Stopping Behavior [{}][{}]".format(wType, wBehaviorName))
            wBehavior.stop(iRobot)
            self._currentBehaviorSet[wType].remove(wBehaviorName)
        
    self._stopBehaviorSet = {}

    for wType in self._startBehaviorSet:
      wList = self._startBehaviorSet[wType]
      for wBehaviorName in wList:        
        if wType in self._currentBehaviorSet:
          for wExistingBehavior in self._currentBehaviorSet[wType]:
            wBehavior = getBehaviorDB().getBehavior(wType, wExistingBehavior)
            print("Stopping Behavior [{}][{}]".format(wType, wExistingBehavior))
            wBehavior.stop(iRobot)
        
        wBehavior = getBehaviorDB().getBehavior(wType, wBehaviorName)
        print("Starting Behavior [{}][{}]".format(wType, wBehaviorName))
        wBehavior.start(iRobot)
        self._currentBehaviorSet[wType] = [wBehaviorName]

    self._startBehaviorSet = {}
    
    for wType in self._currentBehaviorSet:
      wList = self._currentBehaviorSet[wType]
      for wBehavior in wList:
        wBehavior = getBehaviorDB().getBehavior(wType, wBehavior)
        wBehavior.tick(iRobot, iDt, iElapseTime)

    return
