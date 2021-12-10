import json
from os import wait
import time
import math
import threading

from .HWIO.LEDController import LEDController
from .HWIO.SwitchController import SwitchController
from .HWIO.ServoController import ServoController
from .KinematicsDB import getKinematicsDB


eRobotState_VOID = 0
eRobotState_LOAD = 1
eRobotState_WAKE = 2
eRobotState_RUN = 3
eRobotState_DROWZEE = 4
eRobotState_SLEEP = 5

cServoOffPosition = 360

class HardwareModel:

  class EffectorDefinition:
    def __init__(self):
      self.Name = "No Name"
      self.KinematicName = "Not Set"
      self.KinematicReflection_X_Axis = False
      self.KinematicReflection_Y_Axis = False
      self.KinematicReflection_Z_Axis = False
      self.Anchor_X_mm = 0.0
      self.Anchor_Y_mm = 0.0
      self.Anchor_Z_mm = 0.0
      self.servoPositions = []
      self.servo_Controller = None

  def __init__(self):
    
    self._led_left = []
    self._led_right = []
    self._led_Controller = None

    self._switch_state = []
    self._switch_Controller = None

    self._legs = []
    self._servo_controller = None
    return

  def cleanConfig(self):
    
    self._led_left = []
    self._led_right = []
    
    if None != self._led_Controller:
      del self._led_Controller
      self._led_Controller = None

    self._switch_state = []

    if None != self._switch_Controller:
      del self._switch_Controller
      self._switch_Controller = None

    return


  def loadConfig(self, iConfigObject):

    # Extract LED Mapping
    if "LED" in iConfigObject:
      self._led_Controller = LEDController()
      wLedConf = iConfigObject["LED"]
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
    if "Switch GPIO" in iConfigObject:
      wPinArray = []
      self._switch_state = []
      for wPin in iConfigObject["Switch GPIO"]:
        if wPin > 0:
          wPinArray.append(int(wPin))
          self._switch_state.append(False)

      self._switch_Controller = SwitchController(wPinArray)

    # Extract Leg Mapping
    if "Legs" in iConfigObject:
      for wLegDef in iConfigObject["Legs"]:
        wEffectorObj = HardwareModel.EffectorDefinition()
        self._legs.append(wEffectorObj)

        if "Name" in wLegDef:
          wEffectorObj.Name = wLegDef["Name"]
          print("Definition Found for {}".format(wEffectorObj.Name))
        
        if "Kinematic Model" in wLegDef:
          wEffectorObj.KinematicName = wLegDef["Kinematic Model"]
          print("Kinematic used {}".format(wEffectorObj.KinematicName))

        if "Kinematic Reflection X-axis" in wLegDef:
          if True == wLegDef["Kinematic Reflection X-axis"]:
            wEffectorObj.KinematicReflection_X_Axis = True

        if "Kinematic Reflection Y-axis" in wLegDef:
          if True == wLegDef["Kinematic Reflection Y-axis"]:
            wEffectorObj.KinematicReflection_Y_Axis = True

        if "Kinematic Reflection Z-axis" in wLegDef:
          if True == wLegDef["Kinematic Reflection Z-axis"]:
            wEffectorObj.KinematicReflection_Z_Axis = True

        if "Anchor X mm" in wLegDef:
          wEffectorObj.Anchor_X_mm = float(wLegDef["Anchor X mm"])

        if "Anchor Y mm" in wLegDef:
          wEffectorObj.Anchor_X_mm = float(wLegDef["Anchor Y mm"])

        if "Anchor Z mm" in wLegDef:
          wEffectorObj.Anchor_X_mm = float(wLegDef["Anchor Z mm"])


        if "Servos" in wLegDef:
          wServoList = wLegDef["Servos"]
          
          wPortList = []
          for wServo in wServoList:
            wPortList.append(wServo["Port Id"])
          
          wEffectorObj.servo_Controller = ServoController(wPortList)
          wEffectorObj.servoPositions = []

          print("Number of Servos defined {}".format(wEffectorObj.servo_Controller.getServoCount()))

          for wi in range(0, len(wServoList)):
            wEffectorObj.servoPositions.append(0)
            wServoDef = wServoList[wi]
            if "Pulse Width 0 degree" in wServoDef:
              wEffectorObj.servo_Controller.setServo0DegPulseWidth(wi , int(wServoDef["Pulse Width 0 degree"]))
            if "Pulse Width 180 degree" in wServoDef:
              wEffectorObj.servo_Controller.setServo180DegPulseWidth(wi , int(wServoDef["Pulse Width 180 degree"]))
            if "Reference Angle (degree)" in wServoDef:
              wEffectorObj.servo_Controller.setServoReferenceAngle(wi , int(wServoDef["Reference Angle (degree)"]))
            if "Limit Angle Max (degree)" in wServoDef:
              wEffectorObj.servo_Controller.setLimitAngleMax(wi , int(wServoDef["Limit Angle Max (degree)"]))
            if "Limit Angle Min (degree)" in wServoDef:
              wEffectorObj.servo_Controller.setLimitAngleMin(wi , int(wServoDef["Limit Angle Min (degree)"]))

            if False == wEffectorObj.servo_Controller.isServoDefinitionValid(wi):
              print("Servo {} is not properly defined".format(wi))
          
          
    return True


  def wake(self, iRobot):

    self.centerAllLegs()
    self.update_LegServos()
    
    return True


  def sleep(self, iRobot):

    self.setLEDWipe_Left(0,0,0)
    self.setLEDWipe_Right(0,0,0)
    self.update_LED()

    self.setSwitchAll(False)
    self.update_Switchs()

    self.turnOffAllLegs()
    self.update_LegServos()

    return


  def tick(self, iRobot, iDt, iElapseTime):
  
    self.update_LED()
    self.update_Switchs()
    self.update_LegServos()

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


  def update_LegServos(self):
    for wLeg in self._legs:
      #print("Updating leg {}".format(wLeg.Name))
      for wi in range(0, len(wLeg.servoPositions)):
        if cServoOffPosition != wLeg.servoPositions[wi]:
          wLeg.servo_Controller.setServoAngle(wi, wLeg.servoPositions[wi])
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
    if iIndex >= 0:
      if iIndex < len(self._switch_state):
        self._switch_state[iIndex] = iOn
    return
  
  def setSwitchAll(self, iOn = False):
    for wSwitch in self._switch_state:
      wSwitch = iOn
    return


  def getSwitchCount(self):
      return len(self._switch_state)


  def getSwitchState(self, iIndex):
    if iIndex >= 0:
      if iIndex < len(self._switch_state):
        return self._switch_state[iIndex]
    return None


  def setLegServoAngle(self, iLegId, iServoId, iAngle):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        wPositionArray = self._legs[iLegId].servoPositions
        if iServoId >= 0:
          if iServoId < len(wPositionArray):
            wPositionArray[iServoId] = iAngle
    return


  def setLegEffectorPosition(self, iLegId, iX, iY, iZ):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        wEffector = self._legs[iLegId]
        wKinematicModel = getKinematicsDB().getKinematics(wEffector.KinematicName)
        if None != wKinematicModel:
          wX = iX - wEffector.Anchor_X_mm
          wY = iY - wEffector.Anchor_Y_mm
          wZ = iZ - wEffector.Anchor_Z_mm

          if wEffector.KinematicReflection_X_Axis:
            wX = -wX

          if wEffector.KinematicReflection_Y_Axis:
            wY = -wY

          if wEffector.KinematicReflection_Z_Axis:
            wZ = -wZ

          wResult = wKinematicModel.calculateInverseKinematics(wX,wY,wZ)
          if None != wResult:
            wPositionArray = self._legs[iLegId].servoPositions
            wPositionCount = len(wPositionArray)
            for wi in range(0, len(wResult.input)):
              if wi < wPositionCount:
                wPositionArray[wi] = wResult.input[wi]

    return


  def centerLegServo(self, iLegId, iServoId):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        wPositionArray = self._legs[iLegId].servoPositions
        if iServoId >= 0:
          if iServoId < len(wPositionArray):
            wPositionArray[iServoId] = 0
    return


  def centerLeg(self, iLegId):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        wPositionArray = self._legs[iLegId].servoPositions
        for wi in range(0, len(wPositionArray)):
          wPositionArray[wi] = 0
    return


  def centerAllLegs(self):
    for wLeg in self._legs:
      wPositionArray = wLeg.servoPositions
      for wi in range(0, len(wPositionArray)):
        wPositionArray[wi] = 0
    return


  def turnOffLegServo(self, iLegId, iServoId):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        wPositionArray = self._legs[iLegId].servoPositions
        if iServoId >= 0:
          if iServoId < len(wPositionArray):
            wPositionArray[iServoId] = cServoOffPosition
        self._legs[iLegId].turnServoOff(iServoId)
    return


  def turnOffLeg(self, iLegId):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        wPositionArray = self._legs[iLegId].servoPositions
        for wi in range(0, len(wPositionArray)):
          wPositionArray[wi] = cServoOffPosition
        self._legs[iLegId].servo_controller.turnServoOff_All()
    return


  def turnOffAllLegs(self):
    for wLeg in self._legs:
      wPositionArray = wLeg.servoPositions
      for wi in range(0, len(wPositionArray)):
        wPositionArray[wi] = cServoOffPosition
      wLeg.servo_Controller.turnServoOff_All()
    return


  def getLegName(self, iLegId):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        return self._legs[iLegId].Name
    return None


  def getLegCount(self):
    return len(self._legs)

  
  def getLegServoCount(self, iLegId):
    if iLegId >= 0:
      if iLegId < len(self._legs):
        return len(self._legs[iLegId].servoPositions)
    return None
