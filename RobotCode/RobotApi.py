import json
from flask import Blueprint, request, Response

from RobotCode import BehaviorDB
from RobotCode.RobotModel import getRobotModel

Robot_Api_BluePrint = Blueprint('Robot_Api_BluePrint', __name__, url_prefix="/robot_api")

@Robot_Api_BluePrint.route('/getBehaviorMenu')
def getBehaviorMenu():
  return json.dumps(BehaviorDB.getBehaviorDB().getBehaviorMenu())


@Robot_Api_BluePrint.route('/getCurrentBehavior')
def getCurrentBehavior():
  return json.dumps(getRobotModel().getBehavior().getCurrentBahaviorSet())


@Robot_Api_BluePrint.route('/getBehaviorForm/<iBehaviorType>/<iBehaviorName>')
def getBehaviorForm(iBehaviorType, iBehaviorName):
  wBehavior = BehaviorDB.getBehaviorDB().getBehavior(iBehaviorType, iBehaviorName)
  if None != wBehavior:
    return json.dumps(wBehavior.getParametersForm())
  print("Unable to find Behavior [{}] - [{}]".format(iBehaviorType, iBehaviorName))
  return "Unable to find Behavior [{}] - [{}]".format(iBehaviorType, iBehaviorName)


@Robot_Api_BluePrint.route('/setBehavior', methods=["POST"])
def setbehavior():
  wData = request.get_json()
  
  if "Type" in wData:
    if "Name" in wData:
      if "Parameters" in wData:
        if True == getRobotModel().getBehavior().selectBehavior(wData["Type"], wData["Name"], wData["Parameters"]):
          return "Behavior Set"
        return "Behavior not found"
      elif True == getRobotModel().getBehavior().selectBehavior(wData["Type"], wData["Name"]):
        return "Behavior Set"
      return "Behavior not found"
  return "Behavior not defined"


@Robot_Api_BluePrint.route('/hasCameraFeed')
def hasCameraFeed():
  return json.dumps(getRobotModel().getHardware().hasCameraFeed())


@Robot_Api_BluePrint.route('/getCameraFeedRaw')
def getCameraFeedRaw():

  def generateImage():
    while True:
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + getRobotModel().getHardware().getCameraFeedRaw() + b'\r\n')

  return Response( generateImage() , mimetype='multipart/x-mixed-replace; boundary=frame')


@Robot_Api_BluePrint.route('/getCameraFeedProcessed')
def getCameraFeedProcessed():

  def generateImage():
    while True:
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + getRobotModel().getHardware().getCameraFeedProcessed() + b'\r\n')

  return Response( generateImage() , mimetype='multipart/x-mixed-replace; boundary=frame')

