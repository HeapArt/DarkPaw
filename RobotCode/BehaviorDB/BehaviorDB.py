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


  def start(self, iRobot):
    return True


  def stop(self, iRobot):
    return True
  
  
  def tick(self, iRobot, iDt, iElapseTime):
    return True


class BehaviorDB():
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


  def getBehavior(self, iBehaviorType, iBehaviorName):
    if iBehaviorType in self._behaviorDictionary:
      if iBehaviorName in self._behaviorDictionary[iBehaviorType]:
        return self._behaviorDictionary[iBehaviorType][iBehaviorName]

    return None


_gBehaviorDatabase = None
def getBehaviorDB():
  global _gBehaviorDatabase
  if None == _gBehaviorDatabase:
    _gBehaviorDatabase = BehaviorDB()
  return _gBehaviorDatabase

def addBehavior(iBehavior):
  return getBehaviorDB().addBehavior(iBehavior)
