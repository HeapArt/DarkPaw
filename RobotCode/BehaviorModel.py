import time
import math
import copy
from .BehaviorDB import getBehaviorDB

class BehaviorModel():
  def __init__(self):
    self._currentBehaviorSet = {}
    self._stopBehaviorSet = {}
    self._startBehaviorSet = {}
    self._defaultBehaviorSelection = None
    return


  def loadConfig(self, iConfigObject):

    # Setup Initial Behavior
    if "Initial Behavior" in iConfigObject:
      wInitialSetup = iConfigObject["Initial Behavior"]

      self._defaultBehaviorSelection = copy.deepcopy(wInitialSetup)
      
    return True


  def getCurrentBahaviorSet(self):
    return copy.deepcopy(self._currentBehaviorSet)


  def selectBehavior(self, iBehaviorType, iBehaviorName, iParameters = {}):
    wBehavior = getBehaviorDB().getBehavior(iBehaviorType, iBehaviorName)
    if None != wBehavior:
      wSetup = {}
      wSetup["Name"] = iBehaviorName
      wSetup["Parameters"] = iParameters
      self._startBehaviorSet[iBehaviorType] = wSetup

      return True

    return False


  def stopBehavior(self, iBehaviorType, iBehaviorName):
    wBehavior = getBehaviorDB().getBehavior(iBehaviorType, iBehaviorName)
    if None != wBehavior:
      self._stopBehaviorSet[iBehaviorType] = [iBehaviorName]
      return True
    return False


  def setDefaultBehavior(self):

    for wBehavior in self._defaultBehaviorSelection:
      if "Type" not in wBehavior or "Name" not in wBehavior:
        print("Error parsing Initial Behavior : {}".format(json.dumps(wBehavior)))
        return False

      wParameter = {}
      if "Parameters" in wBehavior:
        wParameter = wBehavior["Parameters"]
        
      self.selectBehavior(wBehavior["Type"], wBehavior["Name"], wParameter)


  def wake(self, iRobot):
    if None == iRobot:
      return
    getBehaviorDB().wake(iRobot)
    self.setDefaultBehavior()

    return


  def sleep(self, iRobot):
    if None == iRobot:
      return
    getBehaviorDB().sleep(iRobot)
    return
  
  
  def tick(self, iRobot, iDt, iElapseTime):
    if None == iRobot:
      return

    for wType in self._stopBehaviorSet:
      wList = self._stopBehaviorSet[wType]
      for wBehaviorName in wList:
        if wType in self._startBehaviorSet:
          if wBehaviorName == self._startBehaviorSet[wType]["Name"]:
            del self._startBehaviorSet[wType]
        
        if wType in self._currentBehaviorSet:
          if wBehaviorName == self._currentBehaviorSet[wType]:
            wBehavior = getBehaviorDB().getBehavior(wType, wBehaviorName)
            print("Stopping Behavior [{}][{}]".format(wType, wBehaviorName))
            wBehavior.stop(iRobot)
            del self._currentBehaviorSet[wType]
        
    self._stopBehaviorSet = {}

    for wType in self._startBehaviorSet:
      wBehaviorSetup = self._startBehaviorSet[wType]
      if wType in self._currentBehaviorSet:
        wStopBehavior = getBehaviorDB().getBehavior(wType, self._currentBehaviorSet[wType])
        if None != wStopBehavior:
          print("Stopping Behavior [{}][{}]".format(wType, self._currentBehaviorSet[wType]))
          wStopBehavior.stop(iRobot)
          del self._currentBehaviorSet[wType]
        
      wNewBehavior = getBehaviorDB().getBehavior(wType, wBehaviorSetup["Name"])
      
      print("Starting Behavior [{}][{}] with Parameters : {}".format(wType, wBehaviorSetup["Name"], wBehaviorSetup["Parameters"]))
      wNewBehavior.setParameters(wBehaviorSetup["Parameters"])
      wNewBehavior.start(iRobot)
      self._currentBehaviorSet[wType] = wBehaviorSetup["Name"]

    self._startBehaviorSet = {}
    
    for wType in self._currentBehaviorSet:
      wBehavior = getBehaviorDB().getBehavior(wType, self._currentBehaviorSet[wType])
      wBehavior.tick(iRobot, iDt, iElapseTime)

    return
