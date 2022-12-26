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

      if "" != wType:
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


gCreationCallback = None

class BehaviorDB():
  def __init__(self):
    self._mBehaviorDictionary = {}
    self._mBehaviorMenu = {}
    self._mWakeCallback = []
    return


  def addBehavior(self, iBehavior):

    if False == isinstance(iBehavior, BehaviorTemplate):
      return False

    wType = iBehavior.getBehaviorType()
    if wType not in self._mBehaviorDictionary:
      print("Adding Behavior Type to library [{}]".format(wType))
      self._mBehaviorDictionary[wType] = {}
      self._mBehaviorMenu[wType] = []
    
    wName = iBehavior.getBehaviorName()
    if wName not in self._mBehaviorDictionary[wType]:
      print("Adding Behavior to library Type [{}] Name [{}]".format(wType,wName))
      self._mBehaviorDictionary[wType][wName] = iBehavior
      self._mBehaviorMenu[wType].append(wName)
      self._mBehaviorMenu[wType].sort()
    else:
      print("Behavior already in library Type [{}] Name [{}]".format(wType,wName))
      
    
    return True


  def getBehaviorMenu(self):
    return self._mBehaviorMenu


  def getBehavior(self, iBehaviorType, iBehaviorName):
    if iBehaviorType in self._mBehaviorDictionary:
      if iBehaviorName in self._mBehaviorDictionary[iBehaviorType]:
        return self._mBehaviorDictionary[iBehaviorType][iBehaviorName]

    return None


  def subscribeToWakeCallback(self, iCallback):
    print("Subscribe to Wake Call back for behavior")
    self._mWakeCallback.append(iCallback)


  def wake(self, iRobot):
    print("Performing Wake Call back for behavior")
    for wWakeCallback in self._mWakeCallback:
      wWakeCallback(iRobot)

      
    for wType in self._mBehaviorDictionary:
      for wName in self._mBehaviorDictionary[wType]:
        self._mBehaviorDictionary[wType][wName].wake(iRobot)
    return True


  def sleep(self, iRobot):
    for wType in self._mBehaviorDictionary:
      for wName in self._mBehaviorDictionary[wType]:
        self._mBehaviorDictionary[wType][wName].sleep(iRobot)
    return True


_gBehaviorDatabase = None
def getBehaviorDB():
  global _gBehaviorDatabase
  if None == _gBehaviorDatabase:
    print("Creating Behavior DB")
    _gBehaviorDatabase = BehaviorDB()
  return _gBehaviorDatabase

def addBehavior(iBehavior):
  return getBehaviorDB().addBehavior(iBehavior)
