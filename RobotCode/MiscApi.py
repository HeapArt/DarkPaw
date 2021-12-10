import json
from flask import Blueprint, request

import RobotCode.KinematicsDB.DarkPaw as DarkPaw

Misc_Api_BluePrint = Blueprint('Misc_Api_BluePrint', __name__, url_prefix="/misc_api")


@Misc_Api_BluePrint.route('/kinematicsTesting/DarkPaw/leg/forward/<iInput0>/<iInput1>/<iInput2>')
def kinematicsTesting_DarkPaw_Forward(iInput0, iInput1, iInput2):
  print("DarkPaw/leg/forward calculation input0 [{}] input1 [{}] input2 [{}]".format(iInput0, iInput1, iInput2))

  wResult = DarkPaw.forwardKinematics_full(float(iInput0),float(iInput1),float(iInput2))
  for wkey in wResult["Joints Hinge"]:
    wResult["Joints Hinge"][wkey]["y"] = wResult["Joints Hinge"][wkey]["y"] + 45
  
  wPoints = {}
  wPoints.update(wResult["Joints Hinge"])
  wPoints.update(wResult["Joints Leg"])

  wImage = {}
  wImage["points"] = wPoints
  wImage["lines"] = DarkPaw.linkDefinition()

  return json.dumps(wImage)


@Misc_Api_BluePrint.route('/kinematicsTesting/DarkPaw/leg/inverse/<iInput0>/<iInput1>/<iInput2>')
def kinematicsTesting_DarkPaw_Inverse(iInput0, iInput1, iInput2):
  print("DarkPaw/leg/inverse calculation input1 [{}] input2 [{}]".format(iInput1, iInput2))
  wCenterPosition = DarkPaw.getCenterPosition()
  wX = float(iInput0) + wCenterPosition[0]
  wY = float(iInput1) + wCenterPosition[1]
  wZ = float(iInput2) + wCenterPosition[2]

  wResult = DarkPaw.inverseKinematics_full(wX,wY,wZ)
  wPoints = {}
  if None != wResult:
    for wkey in wResult["Joints Hinge"]:
      wResult["Joints Hinge"][wkey]["y"] = wResult["Joints Hinge"][wkey]["y"] + 45
  
    wPoints.update(wResult["Joints Hinge"])
    wPoints.update(wResult["Joints Leg"])

  wImage = {}
  wImage["points"] = wPoints
  wImage["lines"] = DarkPaw.linkDefinition()

  return json.dumps(wImage)