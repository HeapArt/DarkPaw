import time
import math
from .BehaviorDB import getBehaviorDB

class BehaviorModel():
  def __init__(self):
    self._currentBehaviorSet = {}
    return

  def selectBehavior(self, iBehaviorType, iBehaviorName):
    wBehavior = getBehaviorDB().getBehavior(iBehaviorType, iBehaviorName)
    if None != wBehavior:
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
        wBehavior = getBehaviorDB().getBehavior(wType, wBehavior)
        wBehavior.wake(iRobot)

    return


  def sleep(self, iRobot):
    if None == iRobot:
      return

    for wType in self._currentBehaviorSet:
      wList = self._currentBehaviorSet[wType]
      for wBehavior in wList:
        wBehavior = getBehaviorDB().getBehavior(wType, wBehavior)
        wBehavior.sleep(iRobot)

    return
  
  
  def tick(self, iRobot, iDt, iElapseTime):
    if None == iRobot:
      return

    for wType in self._currentBehaviorSet:
      wList = self._currentBehaviorSet[wType]
      for wBehavior in wList:
        wBehavior = getBehaviorDB().getBehavior(wType, wBehavior)
        wBehavior.tick(iRobot, iDt, iElapseTime)

    return
