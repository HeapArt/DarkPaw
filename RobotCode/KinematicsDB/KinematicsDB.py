import time
import math
import copy
import json

class KinematicsTemplate():
  def __init__(self, iKinematicsName):
    self._mKinematicsName = iKinematicsName
    addKinematics(self)
    return


  def getKinematicsName(self):
    return self._mKinematicsName


  def calculateForwardKinematics(self, iServoPositions=[]):
    return None


  def calculateInverseKinematics(self, iX, iY, iZ):
    return None



class KinematicsDB():
  def __init__(self):
    self._mKinematicsDictionary = {}
    return


  def addKinematics(self, iKinematics):

    if False == isinstance(iKinematics, KinematicsTemplate):
      return False

    wName = iKinematics.getKinematicsName() 
    if wName not in self._mKinematicsDictionary:
      print("Adding Kinematics to library [{}]".format(wName))
      self._mKinematicsDictionary[wName] = iKinematics
      return True

    else:
      print("Kinematics [{}] already exists. Unable to add to library.".format(wName))

    return False


  def getKinematicsMenu(self):
    return self._mKinematicsDictionary.keys()


  def getKinematics(self, iKinematicsName):
    if iKinematicsName in self._mKinematicsDictionary:
      return self._mKinematicsDictionary[iKinematicsName]
    return None


  def wake(self, iRobot):
    return True


  def sleep(self, iRobot):
    return True


_gKinematicsDatabase = None
def getKinematicsDB():
  global _gKinematicsDatabase
  if None == _gKinematicsDatabase:
    _gKinematicsDatabase = KinematicsDB()
  return _gKinematicsDatabase

def addKinematics(iBehavior):
  return getKinematicsDB().addKinematics(iBehavior)
