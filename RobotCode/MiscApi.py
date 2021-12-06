import json
from flask import Blueprint, request

import RobotCode.Kinematics.DarkPaw as DarkPaw

Misc_Api_BluePrint = Blueprint('Misc_Api_BluePrint', __name__, url_prefix="/misc_api")


@Misc_Api_BluePrint.route('/kinematicsTesting/DarkPaw/leg/forward/<iInput1>/<iInput2>')
def kinematicsTesting_DarkPaw_Forward(iInput1, iInput2):
  print("DarkPaw/leg/forward calculation input1 [{}] input2 [{}]".format(iInput1, iInput2))

  wImage = {}
  wImage["points"] = DarkPaw.forwardKinematics_singleLeg(float(iInput1), float(iInput2))
  wImage["lines"] = DarkPaw.linkDefinition()

  return json.dumps(wImage)


@Misc_Api_BluePrint.route('/kinematicsTesting/DarkPaw/leg/inverse/<iInput1>/<iInput2>')
def kinematicsTesting_DarkPaw_Inverse(iInput1, iInput2):
  print("DarkPaw/leg/inverse calculation input1 [{}] input2 [{}]".format(iInput1, iInput2))

  wImage = {}
  wImage["points"] = DarkPaw.inverseKinematics_singleLeg(float(iInput1), float(iInput2))
  wImage["lines"] = DarkPaw.linkDefinition()

  return json.dumps(wImage)