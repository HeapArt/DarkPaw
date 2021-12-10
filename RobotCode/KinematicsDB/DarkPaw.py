import math

cDIM_CRANK_0_X_FROM_PIVOT = -42 #mm
cDIM_CRANK_0_Y_FROM_PIVOT = 0 #mm
cDIM_CRANK_0_ARM = 15 #mm
cDIM_LINK_0 = 40 #mm
cDIM_LEG_HINGE_FROM_PIVOT = 22 #mm 
cDIM_LEG_HINGE_FROM_CENTERLINE = 15 #mm 
cDIM_PIVOT_TO_LEG_ORIGIN = 65 #mm

cDIM_CRANK_1_X = -35 #mm
cDIM_CRANK_1_Y = 6 #mm
cDIM_CRANK_1_ARM = 15 #mm
cDIM_CRANK_2_X = -35 #mm
cDIM_CRANK_2_Y = -6 #mm
cDIM_CRANK_2_ARM = 15 #mm
cDIM_LINK_1 = 25 #mm
cDIM_LINK_2 = 35 #mm
cDIM_Link_3 = 30 #mm
cDIM_Y_LINK_HEIGHT = 35 #mm
cDIM_Y_LINK_WIDTH = 25 #mm
cDIM_TRIANGLE_HEIGHT = 25 #mm 
cDIM_TRIANGLE_WIDTH = 30 #mm

cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN = 40 #mm
cDIM_EFFECTOR_Y_IN_TO_OUT_Y = 100 #mm
cDIM_EFFECTOR_Y_IN_TO_OUT_X = 40 #mm
cDIM_EFFECTOR_BALL_RADIUS = 5 #mm

cINVERSE_X_LIMIT = cDIM_EFFECTOR_BALL_RADIUS #mm
cINVERSE_Y_LIMIT = -2*cDIM_EFFECTOR_BALL_RADIUS #mm

eCRANK_0_ORIGIN = "pC0"
eCRANK_0_OUT = "pC0_Out"
eHINGE_IN = "pH_In"
eHINGE_OUT = "pH_Out"
ePIVOT = "PIVOT"

eORIGIN = "p0"
eCRANK_1_ORIGIN = "pC1"
eCRANK_1_OUT = "p7"
eCRANK_2_ORIGIN = "pC2"
eCRANK_2_OUT = "p3"
eY_LINK_IN = "p6"
eY_LINK_OUT = "p5"
eTRIANGLE_IN = "p2"
eEFFECTOR_IN_Y = "p4"
eEFFECTOR_IN_TRI = eTRIANGLE_OUT = "p1"
eEFFECTOR_OUT = "pEnd"
eEFFECTOR_CONTACT = "pEnd Contact"


def _definePoint(ix,iy):
  wPoint = {}
  wPoint["x"] = ix
  wPoint["y"] = iy
  return wPoint


def _defineComponents_Pivot():
  wComponents = {}
  wComponents["Body"] = [ePIVOT,eCRANK_0_ORIGIN]
  wComponents["Crank 0"] = [eCRANK_0_ORIGIN, eCRANK_0_OUT]
  wComponents["Link 0"] = [eCRANK_0_OUT, eHINGE_IN]
  wComponents["Pivot"] = [ePIVOT, eHINGE_IN, eHINGE_OUT]
  
  return wComponents

def _defineHingeJoints():
  wJoints = {}
  
  wJoints[ePIVOT] = _definePoint(0, 0)
  wJoints[eCRANK_0_ORIGIN] = _definePoint(cDIM_CRANK_0_X_FROM_PIVOT, cDIM_CRANK_0_Y_FROM_PIVOT)
  wJoints[eCRANK_0_OUT] = _definePoint(cDIM_CRANK_0_X_FROM_PIVOT, cDIM_CRANK_0_Y_FROM_PIVOT + cDIM_CRANK_0_ARM)
  wJoints[eHINGE_IN] = _definePoint(wJoints[ePIVOT]["x"] + cDIM_LEG_HINGE_FROM_CENTERLINE, wJoints[ePIVOT]["y"] + cDIM_LEG_HINGE_FROM_PIVOT)
  wJoints[eHINGE_OUT] = _definePoint(wJoints[ePIVOT]["x"] , wJoints[ePIVOT]["y"] + cDIM_LEG_HINGE_FROM_PIVOT)
  
  return wJoints


def _defineComponents_Leg():
  wComponents = {}
  wComponents["Base Plate"] = [eORIGIN,eCRANK_1_ORIGIN,eCRANK_2_ORIGIN]
  wComponents["Crank 1"] = [eCRANK_1_ORIGIN, eCRANK_1_OUT]
  wComponents["Crank 2"] = [eCRANK_2_ORIGIN, eCRANK_2_OUT]
  wComponents["Link 1"] = [eCRANK_1_OUT, eY_LINK_IN]
  wComponents["Y Link"] = [eORIGIN, eY_LINK_IN, eY_LINK_OUT]
  wComponents["Link 3"] = [eY_LINK_OUT, eEFFECTOR_IN_Y]
  wComponents["Link 2"] = [eCRANK_2_OUT, eTRIANGLE_IN]
  wComponents["TRIANGLE"] = [eORIGIN, eTRIANGLE_IN, eTRIANGLE_OUT]
  wComponents["End Effector"] = [eEFFECTOR_IN_Y, eEFFECTOR_IN_TRI, eEFFECTOR_OUT]
  return wComponents  
  

def _defineLegJoints():
  wJoints = {}
  wJoints[eORIGIN] = _definePoint(0, 0)
  wJoints[eCRANK_1_ORIGIN] = _definePoint( cDIM_CRANK_1_X, cDIM_CRANK_1_Y)
  wJoints[eCRANK_1_OUT] = _definePoint( cDIM_CRANK_1_X, cDIM_CRANK_1_Y + cDIM_CRANK_1_ARM)
  wJoints[eCRANK_2_ORIGIN] = _definePoint( cDIM_CRANK_2_X, cDIM_CRANK_2_Y)
  wJoints[eCRANK_2_OUT] = _definePoint( cDIM_CRANK_2_X, cDIM_CRANK_2_Y - cDIM_CRANK_2_ARM)
  wJoints[eY_LINK_IN] = _definePoint(-cDIM_Y_LINK_WIDTH/2, cDIM_Y_LINK_HEIGHT)
  wJoints[eY_LINK_OUT] = _definePoint( cDIM_Y_LINK_WIDTH/2, cDIM_Y_LINK_HEIGHT)
  wJoints[eTRIANGLE_IN] = _definePoint( 0, -cDIM_Y_LINK_HEIGHT)
  wJoints[eTRIANGLE_OUT] = _definePoint( cDIM_TRIANGLE_WIDTH, 0)
  wJoints[eEFFECTOR_IN_Y] = _definePoint( cDIM_Y_LINK_WIDTH/2 + cDIM_Link_3, cDIM_Y_LINK_HEIGHT)
  wJoints[eEFFECTOR_IN_TRI] = wJoints[eTRIANGLE_OUT]
  wJoints[eEFFECTOR_OUT] = _definePoint(cDIM_Y_LINK_WIDTH/2 + cDIM_Link_3, cDIM_Y_LINK_HEIGHT - cDIM_EFFECTOR_Y_IN_TO_OUT_Y)
  wJoints[eEFFECTOR_CONTACT] = _definePoint(wJoints[eEFFECTOR_OUT]["x"], wJoints[eEFFECTOR_OUT]["y"] + cDIM_EFFECTOR_BALL_RADIUS)
  return wJoints

def _defineLegDimensions():
  wDimensions = {}

  return wDimensions
def linkDefinition():
  wReturn = {}
  wReturn.update(_defineComponents_Pivot())
  wReturn.update(_defineComponents_Leg())
  return wReturn

def forwardKinematics_singleLeg(iCrank_1, iCrank_2):
  wCrank_1 = float(iCrank_1)
  wCrank_2 = float(iCrank_2)

  wOutputPoints = _defineLegJoints()

  # Top 4 Bar Linkage

  wOutputPoints[eCRANK_1_OUT]["x"] = cDIM_CRANK_1_ARM*math.sin(wCrank_1) + cDIM_CRANK_1_X
  wOutputPoints[eCRANK_1_OUT]["y"] = cDIM_CRANK_1_ARM*math.cos(wCrank_1) + cDIM_CRANK_1_Y

  wSq_Link_1 = cDIM_LINK_1*cDIM_LINK_1
  
  wSq_p6 = cDIM_Y_LINK_HEIGHT*cDIM_Y_LINK_HEIGHT + cDIM_Y_LINK_WIDTH*cDIM_Y_LINK_WIDTH/4
  wL_p6 = math.sqrt(wSq_p6)

  wSq_p7 = wOutputPoints[eCRANK_1_OUT]["x"]*wOutputPoints[eCRANK_1_OUT]["x"] + wOutputPoints[eCRANK_1_OUT]["y"] * wOutputPoints[eCRANK_1_OUT]["y"] 
  wL_p7 = math.sqrt(wSq_p7)

  wAng_p7p0p6 = math.acos((wSq_p7 + wSq_p6 - wSq_Link_1)/(2*wL_p7 * wL_p6))
  wAng_p7 = math.atan2(wOutputPoints[eCRANK_1_OUT]["y"], wOutputPoints[eCRANK_1_OUT]["x"])

  wAng_p6 = wAng_p7 - wAng_p7p0p6
  wp6_x = wL_p6*math.cos(wAng_p6)
  wp6_y = wL_p6*math.sin(wAng_p6)

  wOutputPoints[eY_LINK_IN]["x"] = wp6_x
  wOutputPoints[eY_LINK_IN]["y"] = wp6_y

  wAng_p6p0p5 = 2*(math.atan((cDIM_Y_LINK_WIDTH/2)/cDIM_Y_LINK_HEIGHT))
  wAng_p5 = wAng_p6 - wAng_p6p0p5

  wSq_p5 = wSq_p6
  wL_p5 = wL_p6

  wp5_x = wL_p5*math.cos(wAng_p5)
  wp5_y = wL_p5*math.sin(wAng_p5)

  wOutputPoints[eY_LINK_OUT]["x"] = wp5_x
  wOutputPoints[eY_LINK_OUT]["y"] = wp5_y

  # Bottom 4 bar Linkage

  wOutputPoints[eCRANK_2_OUT]["x"] = cDIM_CRANK_2_ARM*math.sin(wCrank_2 + math.pi) + cDIM_CRANK_2_X
  wOutputPoints[eCRANK_2_OUT]["y"] = cDIM_CRANK_2_ARM*math.cos(wCrank_2 + math.pi) + cDIM_CRANK_2_Y

  wSq_Link_2 = cDIM_LINK_2*cDIM_LINK_2
  
  wL_p2 = cDIM_TRIANGLE_HEIGHT
  wSq_p2 = wL_p2*wL_p2

  wSq_p3 = wOutputPoints[eCRANK_2_OUT]["x"]*wOutputPoints[eCRANK_2_OUT]["x"] + wOutputPoints[eCRANK_2_OUT]["y"] * wOutputPoints[eCRANK_2_OUT]["y"] 
  wL_p3 = math.sqrt(wSq_p3)

  wAng_p3p0p2 = math.acos((wSq_p3 + wSq_p2 - wSq_Link_2)/(2*wL_p3 * wL_p2))
  wAng_p3 = math.atan2(wOutputPoints[eCRANK_2_OUT]["y"], wOutputPoints[eCRANK_2_OUT]["x"])

  wAng_p2 = wAng_p3 + wAng_p3p0p2
  wp2_x = wL_p2*math.cos(wAng_p2)
  wp2_y = wL_p2*math.sin(wAng_p2)

  wOutputPoints[eTRIANGLE_IN]["x"] = wp2_x
  wOutputPoints[eTRIANGLE_IN]["y"] = wp2_y

  wAng_p1p0p2 = math.pi/2
  wAng_p1 = wAng_p2 + wAng_p1p0p2


  wL_p1 = cDIM_TRIANGLE_WIDTH
  wSq_p1 = wL_p1*wL_p1
  
  wp1_x = wL_p1*math.cos(wAng_p1)
  wp1_y = wL_p1*math.sin(wAng_p1)

  wOutputPoints[eTRIANGLE_OUT]["x"] = wp1_x
  wOutputPoints[eTRIANGLE_OUT]["y"] = wp1_y

  # Effector 4 Bar Linkage
  wAng_p5p0p1 = wAng_p5 - wAng_p1

  wSq_p5p1 = wSq_p5 + wSq_p1 - 2*wL_p5*wL_p1*math.cos(wAng_p5p0p1)
  wL_p5p1 = math.sqrt(wSq_p5p1)

  wL_p4p1 = cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN
  wSq_p4p1 = wL_p4p1*wL_p4p1

  wL_p4p5 = cDIM_Link_3
  wSq_p4p5 = wL_p4p5*wL_p4p5

  wAng_p5p1p4 = math.acos( (wSq_p5p1 + wSq_p4p1 - wSq_p4p5)/(2*wL_p5p1*wL_p4p1))

  wAng_p5p1 = math.atan2(wp5_y - wp1_y, wp5_x - wp1_x)

  wAng_p4p1 = wAng_p5p1 - wAng_p5p1p4

  wp4p1_unit_x = math.cos(wAng_p4p1)
  wp4p1_unit_y = math.sin(wAng_p4p1)

  wp4p1_x = wL_p4p1*wp4p1_unit_x
  wp4p1_y = wL_p4p1*wp4p1_unit_y
  
  wp4_x = wp4p1_x + wp1_x
  wp4_y = wp4p1_y + wp1_y

  wOutputPoints[eEFFECTOR_IN_Y]["x"] = wp4_x
  wOutputPoints[eEFFECTOR_IN_Y]["y"] = wp4_y

  wpE_x = wp4_x - (cDIM_EFFECTOR_Y_IN_TO_OUT_Y * wp4p1_unit_x - cDIM_EFFECTOR_Y_IN_TO_OUT_X*wp4p1_unit_y)
  wpE_y = wp4_y - (cDIM_EFFECTOR_Y_IN_TO_OUT_Y * wp4p1_unit_y + cDIM_EFFECTOR_Y_IN_TO_OUT_X*wp4p1_unit_x)

  wOutputPoints[eEFFECTOR_OUT]["x"] = wpE_x
  wOutputPoints[eEFFECTOR_OUT]["y"] = wpE_y

  wOutputPoints[eEFFECTOR_CONTACT]["x"] = wpE_x
  wOutputPoints[eEFFECTOR_CONTACT]["y"] = wpE_y - cDIM_EFFECTOR_BALL_RADIUS

  wResults = {}
  wResults["Joints"] = wOutputPoints
  wResults["Inputs"] = [iCrank_1,iCrank_2]
  wResults["Output Center"] = wOutputPoints[eEFFECTOR_OUT]
  wResults["Output Contact"] = wOutputPoints[eEFFECTOR_CONTACT]
  return wResults


def inverseKinematics_singleLeg(iXpos, iYpos):

  wOutputPoints = _defineLegJoints()

  wpE_x = float(iXpos)
  wpE_y = float(iYpos) + cDIM_EFFECTOR_BALL_RADIUS

  if wpE_x < cINVERSE_X_LIMIT:
    wpE_x = cINVERSE_X_LIMIT
  if wpE_y > cINVERSE_Y_LIMIT:
    wpE_y = cINVERSE_Y_LIMIT

  wOutputPoints[eEFFECTOR_CONTACT]["x"] = wpE_x
  wOutputPoints[eEFFECTOR_CONTACT]["y"] = wpE_y - cDIM_EFFECTOR_BALL_RADIUS

  # Calculate Solution for External Linkage
  wOutputPoints[eEFFECTOR_OUT]["x"] = wpE_x
  wOutputPoints[eEFFECTOR_OUT]["y"] = wpE_y
  
  wSq_pE = wpE_x*wpE_x + wpE_y*wpE_y
  wL_pE = math.sqrt(wSq_pE)

  wL_pEp1_y = cDIM_EFFECTOR_Y_IN_TO_OUT_Y - cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN
  wL_pEp1_x = cDIM_EFFECTOR_Y_IN_TO_OUT_X

  wSq_pEp1 = wL_pEp1_x*wL_pEp1_x + wL_pEp1_y*wL_pEp1_y
  wL_pEp1 = math.sqrt(wSq_pEp1)

  wL_p1 = cDIM_TRIANGLE_WIDTH
  wSq_p1 = wL_p1*wL_p1

  wCos_pip0pE = (wSq_p1 + wSq_pE - wSq_pEp1)/(2*wL_p1*wL_pE)
  if abs(wCos_pip0pE) > 1.0:
    return None

  wAng_p1p0pE = math.acos(wCos_pip0pE)
  wAng_pE = math.atan2(wpE_y,wpE_x)

  wAng_p1 = wAng_pE + wAng_p1p0pE

  wp1_x = wL_p1*math.cos(wAng_p1)
  wp1_y = wL_p1*math.sin(wAng_p1)

  wOutputPoints[eEFFECTOR_IN_TRI]["x"] = wp1_x
  wOutputPoints[eEFFECTOR_IN_TRI]["y"] = wp1_y

  wAng_p2 = wAng_p1 - math.pi/2

  wL_p2 = cDIM_TRIANGLE_HEIGHT

  wp2_x = wL_p2*math.cos(wAng_p2)
  wp2_y = wL_p2*math.sin(wAng_p2)

  wOutputPoints[eTRIANGLE_IN]["x"] = wp2_x
  wOutputPoints[eTRIANGLE_IN]["y"] = wp2_y

  wAng_pEp1p4 = math.pi - math.atan(cDIM_EFFECTOR_Y_IN_TO_OUT_X / (cDIM_EFFECTOR_Y_IN_TO_OUT_Y - cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN))
  wAng_pEp1 = math.atan2(wpE_y - wp1_y, wpE_x - wp1_x) 
  wAng_p4p1 = wAng_pEp1 + wAng_pEp1p4

  wL_p1p4 = cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN
  wp4_x = wL_p1p4*math.cos(wAng_p4p1) + wp1_x
  wp4_y = wL_p1p4*math.sin(wAng_p4p1) + wp1_y

  wOutputPoints[eEFFECTOR_IN_Y]["x"] = wp4_x
  wOutputPoints[eEFFECTOR_IN_Y]["y"] = wp4_y

  wSq_p4 = wp4_x*wp4_x + wp4_y*wp4_y
  wL_p4 = math.sqrt(wSq_p4)

  wSq_p5 = cDIM_Y_LINK_HEIGHT*cDIM_Y_LINK_HEIGHT + cDIM_Y_LINK_WIDTH*cDIM_Y_LINK_WIDTH/4
  wL_p5 = math.sqrt(wSq_p5)

  wL_p4p5 = cDIM_Link_3
  wSq_p4p5 = wL_p4p5*wL_p4p5

  wCos_p4p0p5 = (wSq_p5 + wSq_p4 - wSq_p4p5)/(2*wL_p4*wL_p5)
  if abs(wCos_p4p0p5) > 1.0:
    return None

  wAng_p4p0p5 = math.acos(wCos_p4p0p5)
  wAng_p4 = math.atan2(wp4_y, wp4_x)
  wAng_p5 = wAng_p4 + wAng_p4p0p5

  wp5_x = wL_p5*math.cos(wAng_p5)
  wp5_y = wL_p5*math.sin(wAng_p5)

  wOutputPoints[eY_LINK_OUT]["x"] = wp5_x
  wOutputPoints[eY_LINK_OUT]["y"] = wp5_y

  wAng_p6p0p5 = 2*(math.atan((cDIM_Y_LINK_WIDTH/2)/cDIM_Y_LINK_HEIGHT))
  wAng_p6 = wAng_p5 + wAng_p6p0p5

  wSq_p6 = wSq_p5
  wL_p6 = wL_p5

  wp6_x = wL_p6*math.cos(wAng_p6)
  wp6_y = wL_p6*math.sin(wAng_p6)

  wOutputPoints[eY_LINK_IN]["x"] = wp6_x
  wOutputPoints[eY_LINK_IN]["y"] = wp6_y

  # Calculate bottom linkage

  wpC2_x = cDIM_CRANK_2_X
  wpC2_y = cDIM_CRANK_2_Y

  wOutputPoints[eCRANK_2_ORIGIN]["x"] = wpC2_x
  wOutputPoints[eCRANK_2_ORIGIN]["y"] = wpC2_y

  wp2pC2_x =  wp2_x - wpC2_x
  wp2pC2_y =  wp2_y - wpC2_y

  wSq_p2pC2 = wp2pC2_x*wp2pC2_x + wp2pC2_y*wp2pC2_y
  wL_p2pC2 = math.sqrt(wSq_p2pC2)

  wAng_p2pC2 = math.atan2(wp2pC2_y, wp2pC2_x)

  wL_p3pC2 = cDIM_CRANK_2_ARM
  wSq_p3pC2 = wL_p3pC2*wL_p3pC2

  wL_p2p3 = cDIM_LINK_2
  wSq_p2p3 = wL_p2p3*wL_p2p3

  wCos_p2pC2p3 = (wSq_p2pC2 + wSq_p3pC2 - wSq_p2p3)/(2*wL_p2pC2*wL_p3pC2)
  if abs(wCos_p2pC2p3) > 1.0:
    return None
  
  wAng_p2pC2p3 = math.acos(wCos_p2pC2p3)

  wAng_p3 = wAng_p2pC2 - wAng_p2pC2p3

  wp3_x = wL_p3pC2*math.cos(wAng_p3) + wpC2_x
  wp3_y = wL_p3pC2*math.sin(wAng_p3) + wpC2_y

  wOutputPoints[eCRANK_2_OUT]["x"] = wp3_x
  wOutputPoints[eCRANK_2_OUT]["y"] = wp3_y

  #Calculate Solution for top Linckage

  wpC1_x = cDIM_CRANK_1_X
  wpC1_y = cDIM_CRANK_1_Y

  wOutputPoints[eCRANK_1_ORIGIN]["x"] = wpC1_x
  wOutputPoints[eCRANK_1_ORIGIN]["y"] = wpC1_y

  wp6pC1_x =  wp6_x - wpC1_x
  wp6pC1_y =  wp6_y - wpC1_y

  wSq_p6pC1 = wp6pC1_x*wp6pC1_x + wp6pC1_y*wp6pC1_y
  wL_p6pC1 = math.sqrt(wSq_p6pC1)

  wAng_p6pC1 = math.atan2(wp6pC1_y, wp6pC1_x)

  wL_p7pC1 = cDIM_CRANK_1_ARM
  wSq_p7pC1 = wL_p7pC1*wL_p7pC1

  wL_p6p7 = cDIM_LINK_1
  wSq_p6p7 = wL_p6p7*wL_p6p7

  wCos_p6pC1p7 = (wSq_p6pC1 + wSq_p7pC1 - wSq_p6p7)/(2*wL_p6pC1*wL_p7pC1)
  if abs(wCos_p6pC1p7) > 1.0:
    return None
  
  wAng_p6pC1p7 = math.acos(wCos_p6pC1p7)

  wAng_p7 = wAng_p6pC1 + wAng_p6pC1p7

  wp7_x = wL_p3pC2*math.cos(wAng_p7) + wpC1_x
  wp7_y = wL_p3pC2*math.sin(wAng_p7) + wpC1_y

  wOutputPoints[eCRANK_1_OUT]["x"] = wp7_x
  wOutputPoints[eCRANK_1_OUT]["y"] = wp7_y

  wCrank_1 = wAng_p7 - math.pi /2
  while wCrank_1 > math.pi:
    wCrank_1 = wCrank_1 - 2*math.pi

  while wCrank_1 < -math.pi:
    wCrank_1 = wCrank_1 + 2*math.pi

  wCrank_2 = wAng_p3 - 3*math.pi /2
  while wCrank_2 > math.pi:
    wCrank_2 = wCrank_2 - 2*math.pi

  while wCrank_2 < -math.pi:
    wCrank_2 = wCrank_2 + 2*math.pi

  wResults = {}
  wResults["Joints"] = wOutputPoints
  wResults["Inputs"] = [wCrank_1,wCrank_2]
  wResults["Output Center"] = wOutputPoints[eEFFECTOR_OUT]
  wResults["Output Contact"] = wOutputPoints[eEFFECTOR_CONTACT]
  return wResults

def forwardKinematics_Pivot(iCrank_0):

  wOutputPoints = _defineHingeJoints()

  wpPivot_x = 0
  wpPivot_y = 0

  wOutputPoints[ePIVOT]["x"] = wpPivot_x
  wOutputPoints[ePIVOT]["y"] = wpPivot_y

  wpC0_x = cDIM_CRANK_0_X_FROM_PIVOT + wpPivot_x
  wpC0_y = cDIM_CRANK_0_Y_FROM_PIVOT + wpPivot_y

  wOutputPoints[eCRANK_0_ORIGIN]["x"] = wpC0_x
  wOutputPoints[eCRANK_0_ORIGIN]["y"] = wpC0_y

  wAng_p1pC0 = iCrank_0 + math.pi/2
  wL_pC0p1 = cDIM_CRANK_0_ARM
  wp1_x = wL_pC0p1*math.cos(wAng_p1pC0) + wpC0_x
  wp1_y = wL_pC0p1*math.sin(wAng_p1pC0) + wpC0_y

  wOutputPoints[eCRANK_0_OUT]["x"] = wp1_x
  wOutputPoints[eCRANK_0_OUT]["y"] = wp1_y

  wAng_p1 = math.atan2(wp1_y, wp1_x)

  wSq_p1 = wp1_x*wp1_x + wp1_y*wp1_y
  wL_p1 = math.sqrt(wSq_p1)

  wL_p1p2 = cDIM_LINK_0
  wSq_p1p2 = wL_p1p2*wL_p1p2
  
  wSq_p2 = cDIM_LEG_HINGE_FROM_PIVOT*cDIM_LEG_HINGE_FROM_PIVOT + cDIM_LEG_HINGE_FROM_CENTERLINE*cDIM_LEG_HINGE_FROM_CENTERLINE
  wL_p2 = math.sqrt(wSq_p2)

  wAng_p1pPivotp2 = math.acos((wSq_p1 + wSq_p2 - wSq_p1p2)/(2*wL_p1*wL_p2))
  wAng_p2 = wAng_p1 - wAng_p1pPivotp2

  wp2_x = wL_p2*math.cos(wAng_p2) + wpPivot_x
  wp2_y = wL_p2*math.sin(wAng_p2) + wpPivot_y

  wOutputPoints[eHINGE_IN]["x"] = wp2_x
  wOutputPoints[eHINGE_IN]["y"] = wp2_y

  wL_p3 = cDIM_LEG_HINGE_FROM_PIVOT
  wAng_p2pPivotp3 = math.atan( cDIM_LEG_HINGE_FROM_CENTERLINE/cDIM_LEG_HINGE_FROM_PIVOT)
  
  wAng_p3 = wAng_p2 - wAng_p2pPivotp3

  wp3_x = wL_p3*math.cos(wAng_p3) + wpPivot_x
  wp3_y = wL_p3*math.sin(wAng_p3) + wpPivot_y
  
  wOutputPoints[eHINGE_OUT]["x"] = wp3_x
  wOutputPoints[eHINGE_OUT]["y"] = wp3_y

  wResults = {}
  wResults["Joints"] = wOutputPoints
  wResults["Inputs"] = [iCrank_0]
  wResults["Output Angle"] = wAng_p3
  return wResults


def inverseKinematics_Pivot(iHingeAngle):
  wOutputPoints = _defineHingeJoints()

  wOutputPoints[ePIVOT]["x"] = wpPivot_x = 0
  wOutputPoints[ePIVOT]["y"] = wpPivot_y = 0 

  wpC0_x = cDIM_CRANK_0_X_FROM_PIVOT + wpPivot_x
  wpC0_y = cDIM_CRANK_0_Y_FROM_PIVOT + wpPivot_y

  wOutputPoints[eCRANK_0_ORIGIN]["x"] = wpC0_x
  wOutputPoints[eCRANK_0_ORIGIN]["y"] = wpC0_y

  wL_p3 = cDIM_LEG_HINGE_FROM_PIVOT
  wAng_p3 = iHingeAngle
  wp3_x = wL_p3*math.cos(wAng_p3) + wpPivot_x
  wp3_y = wL_p3*math.sin(wAng_p3) + wpPivot_y

  wOutputPoints[eHINGE_OUT]["x"] = wp3_x
  wOutputPoints[eHINGE_OUT]["y"] = wp3_y

  wAng_p2pPivotp3 = math.atan( cDIM_LEG_HINGE_FROM_CENTERLINE/cDIM_LEG_HINGE_FROM_PIVOT)
  wAng_p2 = wAng_p3 + wAng_p2pPivotp3

  wSq_p2 = cDIM_LEG_HINGE_FROM_PIVOT*cDIM_LEG_HINGE_FROM_PIVOT + cDIM_LEG_HINGE_FROM_CENTERLINE*cDIM_LEG_HINGE_FROM_CENTERLINE
  wL_p2 = math.sqrt(wSq_p2)

  wp2_x = wL_p2*math.cos(wAng_p2) + wpPivot_x
  wp2_y = wL_p2*math.sin(wAng_p2) + wpPivot_y

  wOutputPoints[eHINGE_IN]["x"] = wp2_x
  wOutputPoints[eHINGE_IN]["y"] = wp2_y

  wL_p1pC0 = cDIM_CRANK_0_ARM
  wSq_p1pC0 = wL_p1pC0*wL_p1pC0

  wL_p1p2 = cDIM_LINK_0
  wSq_p1p2 = wL_p1p2*wL_p1p2

  wp2pC0_x = wp2_x - wpC0_x
  wp2pC0_y = wp2_y - wpC0_y

  wSq_p2pC0 = wp2pC0_x*wp2pC0_x + wp2pC0_y*wp2pC0_y
  wL_p2pC0 = math.sqrt(wSq_p2pC0)

  wCos_p1pC0p2 = (wSq_p1pC0 + wSq_p2pC0 - wSq_p1p2)/(2*wL_p2pC0*wL_p1pC0)
  if abs(wCos_p1pC0p2) > 1.0:
    return None

  wAng_p1pC0p2 = math.acos(wCos_p1pC0p2)

  wAng_p2pC0 = math.atan2(wp2pC0_y, wp2pC0_x)
  wAng_p1pC0 = wAng_p2pC0 + wAng_p1pC0p2

  wp1_x = wL_p1pC0*math.cos(wAng_p1pC0) + wpC0_x
  wp1_y = wL_p1pC0*math.sin(wAng_p1pC0) + wpC0_y

  wOutputPoints[eCRANK_0_OUT]["x"] = wp1_x
  wOutputPoints[eCRANK_0_OUT]["y"] = wp1_y

  wCrank_0 = wAng_p1pC0 - math.pi/2
  while(wCrank_0 > math.pi):
    wCrank_0 = wCrank_0 - 2* math.pi

  while(wCrank_0 < -math.pi):
    wCrank_0 = wCrank_0 + 2* math.pi
    

  wResults = {}
  wResults["Joints"] = wOutputPoints
  wResults["Inputs"] = [wCrank_0]
  wResults["Output Angle"] = wAng_p3
  return wResults


def forwardKinematics_full(iCrank_0, iCrank_1, iCrank_2):
  wHingeCalculations = forwardKinematics_Pivot(iCrank_0)
  wHingeOuputAngle = wHingeCalculations["Output Angle"]

  wLegCalculations = forwardKinematics_singleLeg(iCrank_1, iCrank_2)
  wLegOutputPosition = wLegCalculations["Output Contact"]

  wRadius = wLegOutputPosition["x"] + cDIM_PIVOT_TO_LEG_ORIGIN
  wOuputPoint_X = wRadius*math.cos(wHingeOuputAngle)
  wOuputPoint_Y = -wRadius*math.sin(wHingeOuputAngle)
  wOuputPoint_Z = -wLegOutputPosition["y"]

  wResults = {}
  wResults["Joints Hinge"] = wHingeCalculations["Joints"]
  wResults["Joints Leg"] = wLegCalculations["Joints"]
  wResults["Inputs"] = [iCrank_0,iCrank_1, iCrank_2]
  wResults["Output"] = [wOuputPoint_X, wOuputPoint_Y, wOuputPoint_Z]
  return wResults


def inverseKinematics_full(iX, iY, iZ):
  wHingeAngle = math.atan2(-iY, iX)
  wHingeCalculations = inverseKinematics_Pivot(wHingeAngle)
  if None == wHingeCalculations:
    return None

  wHingeOuputAngle = wHingeCalculations["Output Angle"]
  wCrank_0 = wHingeCalculations["Inputs"][0]

  wXpos = math.sqrt(iX*iX + iY*iY) - cDIM_PIVOT_TO_LEG_ORIGIN
  wYpos = -iZ
  wLegCalculations = inverseKinematics_singleLeg(wXpos, wYpos)
  if None == wLegCalculations:
    return None

  wCrank_1 = wLegCalculations["Inputs"][0]
  wCrank_2= wLegCalculations["Inputs"][1]

  wResults = {}
  wResults["Joints Hinge"] = wHingeCalculations["Joints"]
  wResults["Joints Leg"] = wLegCalculations["Joints"]
  wResults["Inputs"] = [wCrank_0, wCrank_1, wCrank_2]
  wResults["Output"] = [iX, iY, iZ]
  return wResults


_cCenterPosition = forwardKinematics_full(0, 0, 0)["Output"]
print(_cCenterPosition)

def getCenterPosition():
  return [_cCenterPosition[0],_cCenterPosition[1],_cCenterPosition[2]]

class DarkPaw():
  def __init__(self):
    super.__init__("DarkPaw")
    return

  def calculateForwardKinematics(self, iServoPositions=[]):

    wResult = forwardKinematics_singleLeg(iCrank_1, iCrank_2)
    return None


  def calculateInverseKinematics(self, iX, iY, iZ):

    wResult = inverseKinematics_singleLeg(iX, iY)

    return None
