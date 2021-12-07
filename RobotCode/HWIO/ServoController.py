import Adafruit_PCA9685

_gPWMController = None
def _getPWMController():
  global _gPWMController
  if None == _gPWMController:
    _gPWMController = Adafruit_PCA9685.PCA9685()
    _gPWMController.set_pwm_freq(50)
  return _gPWMController

class ServoDefinition():
  def __init__(self, iPort_Id = 0):
    self.PortId = iPort_Id
    self.PulseWidth_0_degree = 100
    self.PulseWidth_180_degree = 500
    self.ReferenceAngle_degree = 0
    self.LimitAngleMin_degree = 0
    self.LimitAngleMax_degree = 180
    self.Angle = 0
    self.DefinitionValid = False


class ServoController():
  def __init__(self, iServoPortList= []):
    self._servolist = []
    for wServoPort in iServoPortList:
      wServoDef = ServoDefinition(wServoPort)
      if wServoPort >= 0:
        wServoDef.DefinitionValid = True

      self._servolist.append(wServoDef)
    return
  
  def setServo0DegPulseWidth(self, iServoId, iPulseWidth = 150):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        self._servolist[iServoId].PulseWidth_0_degree = iPulseWidth
        if iPulseWidth < 0:
          self._servolist[iServoId].DefinitionValid = False
        else:
          self._servolist[iServoId].DefinitionValid = True          
        return True
    return False

  def setServo180DegPulseWidth(self, iServoId, iPulseWidth):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        self._servolist[iServoId].PulseWidth_180_degree = iPulseWidth
        if iPulseWidth < 0:
          self._servolist[iServoId].DefinitionValid = False
        else:
          self._servolist[iServoId].DefinitionValid = True
        return True
    return False

  def setServoReferenceAngle(self, iServoId, iAngleDeg):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        wSet = False
        if iAngleDeg >= 0:
          if  iAngleDeg <= 180:
            self._servolist[iServoId].ReferenceAngle_degree = iAngleDeg
            wSet = True

        if False == wSet:
          self._servolist[iServoId].DefinitionValid = False
          return False
        else:
          self._servolist[iServoId].DefinitionValid = True
          return True
        
    return False


  def setLimitAngleMin(self, iServoId, iAngleDeg):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        wSet = False
        if iAngleDeg >= 0:
          if  iAngleDeg <= 180:
            self._servolist[iServoId].LimitAngleMin_degree = iAngleDeg
            wSet = True

        if False == wSet:
          self._servolist[iServoId].DefinitionValid = False
          return False
        else:
          self._servolist[iServoId].DefinitionValid = True
          return True
        
    return False


  def setLimitAngleMax(self, iServoId, iAngleDeg):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        wSet = False
        if iAngleDeg >= 0:
          if  iAngleDeg <= 180:
            self._servolist[iServoId].LimitAngleMax_degree = iAngleDeg
            wSet = True

        if False == wSet:
          self._servolist[iServoId].DefinitionValid = False
          return False
        else:
          self._servolist[iServoId].DefinitionValid = True
          return True
        
    return False

  def setServoAngle(self, iServoId, iAngleDeg):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        wServoDef = self._servolist[iServoId]
        
        if True == wServoDef.DefinitionValid:

          wAngle = iAngleDeg + wServoDef.ReferenceAngle_degree
          if wAngle < 0:
            wAngle = 0
            
          if  wAngle > 180:
            wAngle = 180

          if wAngle < wServoDef.LimitAngleMin_degree:
            wAngle = wServoDef.LimitAngleMin_degree
            
          if  wAngle > wServoDef.LimitAngleMax_degree:
            wAngle = wServoDef.LimitAngleMax_degree

          wServoDef.Angle = wAngle
          wPWM = (wAngle/180)*(wServoDef.PulseWidth_180_degree - wServoDef.PulseWidth_0_degree) + wServoDef.PulseWidth_0_degree
          wPWM = int(wPWM)

          _getPWMController().set_pwm(wServoDef.PortId, 0, wPWM)
          print(wPWM)
          return True
    return False


  def turnServoOff(self, iServoId):
    if iServoId >= 0:
      if iServoId < len(self._servolist):
        wServoDef = self._servolist[iServoId]
        _getPWMController().set_pwm(wServoDef.PortId, 0, 0)
        return True
    return False


  def turnServoOff_All(self):
    for wServoDef in self._servolist:
      _getPWMController().set_pwm(wServoDef.PortId, 0, 0)
    return False


def testFunc():

  servo = ServoController([0,1,2])
  while True:
    wInput = input("Enter Servo No and Position (\"exit\" to quit ): ")
    if "exit" == wInput:
      break
    wInputArr = wInput.split()

    if "off" == wInputArr[1]:
      servo.turnServoOff(int(wInputArr[0]))

    elif "ref" == wInputArr[1]:
      servo.setServoReferenceAngle(int(wInputArr[0]), int(wInputArr[2]))

    elif "min" == wInputArr[1]:
      servo.setLimitAngleMin(int(wInputArr[0]), int(wInputArr[2]))

    elif "max" == wInputArr[1]:
      servo.setLimitAngleMax(int(wInputArr[0]), int(wInputArr[2]))

    else:
      servo.setServoAngle(int(wInputArr[0]), int(wInputArr[1]))

  servo.turnServoOff_All()

if __name__ == '__main__':
    testFunc()