import time
import math


class BehaviorTemplate():
  def __init__(self, iBehaviorType, iBehaviorName):
    self._behaviorType = iBehaviorType
    self._behaviorName = iBehaviorName
    addBehavior(self)
    return


  def getBehaviorType(self):
    return self._behaviorType


  def getBehaviorName(self):
    return self._behaviorName


  def wake(self, iRobot):
    return True


  def sleep(self, iRobot):
    return True
  
  
  def tick(self, iRobot, iDt, iElapseTime):
    return True


class BehaviorModel():
  def __init__(self):
    self._behaviorDictionary = {}
    self._behaviorMenu = {}
    self._currentBehaviorSet = {}
    return


  def addBehavior(self, iBehavior):

    if False == isinstance(iBehavior, BehaviorTemplate):
      return False

    wType = iBehavior.getBehaviorType()
    if wType not in self._behaviorDictionary:
      print("Adding Behavior Type to library []".format(wType))
      self._behaviorDictionary[wType] = {}
      self._behaviorMenu[wType] = []
    
    wName = iBehavior.getBehaviorName()
    if wName not in self._behaviorDictionary[wType]:
      print("Adding Behavior to library Type [{}] Name [{}]".format(wType,wName))
      self._behaviorDictionary[wType][wName] = iBehavior
      self._behaviorMenu[wType].append(wName)
    
    return True


  def getBehaviorMenu(self):
    return self._behaviorMenu


  def selectBehavior(self, iBehaviorType, iBehaviorName):
    if iBehaviorType in self._behaviorDictionary:
      if iBehaviorName in self._behaviorDictionary[iBehaviorType]:
        self._currentBehaviorSet[iBehaviorType] = [iBehaviorName]
        print("Setting Behavior to [{}][{}]".format(iBehaviorType, iBehaviorName))
        return True

    return False


  def wake(self, iRobot):
    if None == iRobot:
      return

    for wType in self._currentBehaviorSet:
       wList = self._currentBehaviorSet[wType]
       for wBehavior in wList:
          self._behaviorDictionary[wType][wBehavior].wake(iRobot)

    return


  def sleep(self, iRobot):
    if None == iRobot:
      return

    for wType in self._currentBehaviorSet:
       wList = self._currentBehaviorSet[wType]
       for wBehavior in wList:
         self._behaviorDictionary[wType][wBehavior].sleep(iRobot)

    return
  
  
  def tick(self, iRobot, iDt, iElapseTime):
    if None == iRobot:
      return

    for wType in self._currentBehaviorSet:
       wList = self._currentBehaviorSet[wType]
       for wBehavior in wList:
         self._behaviorDictionary[wType][wBehavior].tick(iRobot, iDt, iElapseTime)

    return


_gBehaviorModel = None
def getBehaviorModel():
  global _gBehaviorModel
  if None == _gBehaviorModel:
    _gBehaviorModel = BehaviorModel()
  return _gBehaviorModel

def addBehavior(iBehavior):
  return getBehaviorModel().addBehavior(iBehavior)
