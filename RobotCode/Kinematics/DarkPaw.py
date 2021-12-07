import math

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
  
def _defineMagnitude(iContainer, iP1, iP2, iLength):
  if iP1 not in iContainer:
    iContainer[iP1] = {}
  iContainer[iP1][iP2] = iLength

  if iP2 not in iContainer:
    iContainer[iP2] = {}
  iContainer[iP2][iP1] = iLength  

  return


def _defineComponents():
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
  return _defineComponents()

def forwardKinematics_singleLeg(iCrank_1, iCrank_2):
  wCrank_1 = float(iCrank_1)
  wCrank_2 = float(iCrank_2)

  wOuputPoints = _defineLegJoints()

  # Top 4 Bar Linkage

  wOuputPoints[eCRANK_1_OUT]["x"] = cDIM_CRANK_1_ARM*math.sin(wCrank_1) + cDIM_CRANK_1_X
  wOuputPoints[eCRANK_1_OUT]["y"] = cDIM_CRANK_1_ARM*math.cos(wCrank_1) + cDIM_CRANK_1_Y

  wSq_Link_1 = cDIM_LINK_1*cDIM_LINK_1
  
  wSq_p6 = cDIM_Y_LINK_HEIGHT*cDIM_Y_LINK_HEIGHT + cDIM_Y_LINK_WIDTH*cDIM_Y_LINK_WIDTH/4
  wL_p6 = math.sqrt(wSq_p6)

  wSq_p7 = wOuputPoints[eCRANK_1_OUT]["x"]*wOuputPoints[eCRANK_1_OUT]["x"] + wOuputPoints[eCRANK_1_OUT]["y"] * wOuputPoints[eCRANK_1_OUT]["y"] 
  wL_p7 = math.sqrt(wSq_p7)

  wAng_p7p0p6 = math.acos((wSq_p7 + wSq_p6 - wSq_Link_1)/(2*wL_p7 * wL_p6))
  wAng_p7 = math.atan2(wOuputPoints[eCRANK_1_OUT]["y"], wOuputPoints[eCRANK_1_OUT]["x"])

  wAng_p6 = wAng_p7 - wAng_p7p0p6
  wp6_x = wL_p6*math.cos(wAng_p6)
  wp6_y = wL_p6*math.sin(wAng_p6)

  wOuputPoints[eY_LINK_IN]["x"] = wp6_x
  wOuputPoints[eY_LINK_IN]["y"] = wp6_y

  wAng_p6p0p5 = 2*(math.atan((cDIM_Y_LINK_WIDTH/2)/cDIM_Y_LINK_HEIGHT))
  wAng_p5 = wAng_p6 - wAng_p6p0p5

  wSq_p5 = wSq_p6
  wL_p5 = wL_p6

  wp5_x = wL_p5*math.cos(wAng_p5)
  wp5_y = wL_p5*math.sin(wAng_p5)

  wOuputPoints[eY_LINK_OUT]["x"] = wp5_x
  wOuputPoints[eY_LINK_OUT]["y"] = wp5_y

  # Bottom 4 bar Linkage

  wOuputPoints[eCRANK_2_OUT]["x"] = cDIM_CRANK_2_ARM*math.sin(wCrank_2 + math.pi) + cDIM_CRANK_2_X
  wOuputPoints[eCRANK_2_OUT]["y"] = cDIM_CRANK_2_ARM*math.cos(wCrank_2 + math.pi) + cDIM_CRANK_2_Y

  wSq_Link_2 = cDIM_LINK_2*cDIM_LINK_2
  
  wL_p2 = cDIM_TRIANGLE_HEIGHT
  wSq_p2 = wL_p2*wL_p2

  wSq_p3 = wOuputPoints[eCRANK_2_OUT]["x"]*wOuputPoints[eCRANK_2_OUT]["x"] + wOuputPoints[eCRANK_2_OUT]["y"] * wOuputPoints[eCRANK_2_OUT]["y"] 
  wL_p3 = math.sqrt(wSq_p3)

  wAng_p3p0p2 = math.acos((wSq_p3 + wSq_p2 - wSq_Link_2)/(2*wL_p3 * wL_p2))
  wAng_p3 = math.atan2(wOuputPoints[eCRANK_2_OUT]["y"], wOuputPoints[eCRANK_2_OUT]["x"])

  wAng_p2 = wAng_p3 + wAng_p3p0p2
  wp2_x = wL_p2*math.cos(wAng_p2)
  wp2_y = wL_p2*math.sin(wAng_p2)

  wOuputPoints[eTRIANGLE_IN]["x"] = wp2_x
  wOuputPoints[eTRIANGLE_IN]["y"] = wp2_y

  wAng_p1p0p2 = math.pi/2
  wAng_p1 = wAng_p2 + wAng_p1p0p2


  wL_p1 = cDIM_TRIANGLE_WIDTH
  wSq_p1 = wL_p1*wL_p1
  
  wp1_x = wL_p1*math.cos(wAng_p1)
  wp1_y = wL_p1*math.sin(wAng_p1)

  wOuputPoints[eTRIANGLE_OUT]["x"] = wp1_x
  wOuputPoints[eTRIANGLE_OUT]["y"] = wp1_y

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

  wOuputPoints[eEFFECTOR_IN_Y]["x"] = wp4_x
  wOuputPoints[eEFFECTOR_IN_Y]["y"] = wp4_y

  wpE_x = wp4_x - (cDIM_EFFECTOR_Y_IN_TO_OUT_Y * wp4p1_unit_x - cDIM_EFFECTOR_Y_IN_TO_OUT_X*wp4p1_unit_y)
  wpE_y = wp4_y - (cDIM_EFFECTOR_Y_IN_TO_OUT_Y * wp4p1_unit_y + cDIM_EFFECTOR_Y_IN_TO_OUT_X*wp4p1_unit_x)

  wOuputPoints[eEFFECTOR_OUT]["x"] = wpE_x
  wOuputPoints[eEFFECTOR_OUT]["y"] = wpE_y

  wOuputPoints[eEFFECTOR_CONTACT]["x"] = wpE_x
  wOuputPoints[eEFFECTOR_CONTACT]["y"] = wpE_y - cDIM_EFFECTOR_BALL_RADIUS

  return wOuputPoints


def inverseKinematics_singleLeg(iXpos, iYpos):

  wOuputPoints = _defineLegJoints()

  wpE_x = float(iXpos)
  wpE_y = float(iYpos) + cDIM_EFFECTOR_BALL_RADIUS

  if wpE_x < cINVERSE_X_LIMIT:
    wpE_x = cINVERSE_X_LIMIT
  if wpE_y > cINVERSE_Y_LIMIT:
    wpE_y = cINVERSE_Y_LIMIT

  wOuputPoints[eEFFECTOR_CONTACT]["x"] = wpE_x
  wOuputPoints[eEFFECTOR_CONTACT]["y"] = wpE_y - cDIM_EFFECTOR_BALL_RADIUS

  # Calculate Solution for External Linkage
  wOuputPoints[eEFFECTOR_OUT]["x"] = wpE_x
  wOuputPoints[eEFFECTOR_OUT]["y"] = wpE_y
  
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

  wOuputPoints[eEFFECTOR_IN_TRI]["x"] = wp1_x
  wOuputPoints[eEFFECTOR_IN_TRI]["y"] = wp1_y

  wAng_p2 = wAng_p1 - math.pi/2

  wL_p2 = cDIM_TRIANGLE_HEIGHT

  wp2_x = wL_p2*math.cos(wAng_p2)
  wp2_y = wL_p2*math.sin(wAng_p2)

  wOuputPoints[eTRIANGLE_IN]["x"] = wp2_x
  wOuputPoints[eTRIANGLE_IN]["y"] = wp2_y

  wAng_pEp1p4 = math.pi - math.atan(cDIM_EFFECTOR_Y_IN_TO_OUT_X / (cDIM_EFFECTOR_Y_IN_TO_OUT_Y - cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN))
  wAng_pEp1 = math.atan2(wpE_y - wp1_y, wpE_x - wp1_x) 
  wAng_p4p1 = wAng_pEp1 + wAng_pEp1p4

  wL_p1p4 = cDIM_EFFECTOR_Y_IN_TO_TRIANGEL_IN
  wp4_x = wL_p1p4*math.cos(wAng_p4p1) + wp1_x
  wp4_y = wL_p1p4*math.sin(wAng_p4p1) + wp1_y

  wOuputPoints[eEFFECTOR_IN_Y]["x"] = wp4_x
  wOuputPoints[eEFFECTOR_IN_Y]["y"] = wp4_y

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

  wOuputPoints[eY_LINK_OUT]["x"] = wp5_x
  wOuputPoints[eY_LINK_OUT]["y"] = wp5_y

  wAng_p6p0p5 = 2*(math.atan((cDIM_Y_LINK_WIDTH/2)/cDIM_Y_LINK_HEIGHT))
  wAng_p6 = wAng_p5 + wAng_p6p0p5

  wSq_p6 = wSq_p5
  wL_p6 = wL_p5

  wp6_x = wL_p6*math.cos(wAng_p6)
  wp6_y = wL_p6*math.sin(wAng_p6)

  wOuputPoints[eY_LINK_IN]["x"] = wp6_x
  wOuputPoints[eY_LINK_IN]["y"] = wp6_y

  # Calculate bottom linkage

  wpC2_x = cDIM_CRANK_2_X
  wpC2_y = cDIM_CRANK_2_Y

  wOuputPoints[eCRANK_2_ORIGIN]["x"] = wpC2_x
  wOuputPoints[eCRANK_2_ORIGIN]["y"] = wpC2_y

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

  wOuputPoints[eCRANK_2_OUT]["x"] = wp3_x
  wOuputPoints[eCRANK_2_OUT]["y"] = wp3_y

  #Calculate Solution for top Linckage

  wpC1_x = cDIM_CRANK_1_X
  wpC1_y = cDIM_CRANK_1_Y

  wOuputPoints[eCRANK_1_ORIGIN]["x"] = wpC1_x
  wOuputPoints[eCRANK_1_ORIGIN]["y"] = wpC1_y

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

  wOuputPoints[eCRANK_1_OUT]["x"] = wp7_x
  wOuputPoints[eCRANK_1_OUT]["y"] = wp7_y

  return wOuputPoints