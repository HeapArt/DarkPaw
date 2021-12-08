import time
import math
import copy
import json

class BehaviorTemplate():
  def __init__(self, iBehaviorType, iBehaviorName):
    self._mBehaviorType = iBehaviorType
    self._mBehaviorName = iBehaviorName
    self._mParameters = {}
    addBehavior(self)
    return


  def getBehaviorType(self):
    return self._mBehaviorType


  def getBehaviorName(self):
    return self._mBehaviorName


  def getParametersForm(self):
    wFormObject = {}
    
    for wKey in self._mParameters:
      wType = ""

      if isinstance(self._mParameters[wKey], bool):
        wType = "boolean"
      elif isinstance(self._mParameters[wKey], int):
        wType = "integer"
      elif isinstance(self._mParameters[wKey], float):
        wType = "float"
      elif isinstance(self._mParameters[wKey], str):
        wType = "string"

      if "" is not wType:
        wFormObject[wKey] = {}
        wFormObject[wKey]["type"] = wType
        wFormObject[wKey]["value"] = self._mParameters[wKey]
  
    return wFormObject


  def defineParametersForm(self, iParameterObj):
    self._mParameters = iParameterObj
    return

    
  def getParameters(self):
    return self._mParameters


  def setParameters(self, iParameters):
    for wKey in self._mParameters:
      if wKey in iParameters:
        if isinstance(self._mParameters[wKey], bool):
          self._mParameters[wKey] = False
          if True == iParameters[wKey]:
            self._mParameters[wKey] = True
            
        elif isinstance(self._mParameters[wKey], int):
          self._mParameters[wKey] = int(iParameters[wKey])

        elif isinstance(self._mParameters[wKey], float):
          self._mParameters[wKey] = float(iParameters[wKey])

        elif isinstance(self._mParameters[wKey], str):
          self._mParameters[wKey] = str(iParameters[wKey])
    return 

  def wake(self, iRobot):
    return True

  def sleep(self, iRobot):
    return True

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
    return


  def addBehavior(self, iBehavior):

    if False == isinstance(iBehavior, BehaviorTemplate):
      return False

    wType = iBehavior.getBehaviorType()
    if wType not in self._behaviorDictionary:
      print("Adding Behavior Type to library [{}]".format(wType))
      self._behaviorDictionary[wType] = {}
      self._behaviorMenu[wType] = []
    
    wName = iBehavior.getBehaviorName()
    if wName not in self._behaviorDictionary[wType]:
      print("Adding Behavior to library Type [{}] Name [{}]".format(wType,wName))
      self._behaviorDictionary[wType][wName] = iBehavior
      self._behaviorMenu[wType].append(wName)
      self._behaviorMenu[wType].sort()
    
    return True


  def getBehaviorMenu(self):
    return self._behaviorMenu


  def getBehavior(self, iBehaviorType, iBehaviorName):
    if iBehaviorType in self._behaviorDictionary:
      if iBehaviorName in self._behaviorDictionary[iBehaviorType]:
        return self._behaviorDictionary[iBehaviorType][iBehaviorName]

    return None


  def wake(self, iRobot):
    for wType in self._behaviorDictionary:
      for wName in self._behaviorDictionary[wType]:
        self._behaviorDictionary[wType][wName].wake(iRobot)
    return True


  def sleep(self, iRobot):
    for wType in self._behaviorDictionary:
      for wName in self._behaviorDictionary[wType]:
        self._behaviorDictionary[wType][wName].sleep(iRobot)
    return True


_gBehaviorDatabase = None
def getBehaviorDB():
  global _gBehaviorDatabase
  if None == _gBehaviorDatabase:
    _gBehaviorDatabase = BehaviorDB()
  return _gBehaviorDatabase

def addBehavior(iBehavior):
  return getBehaviorDB().addBehavior(iBehavior)
