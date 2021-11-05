import os
from RobotCode.RobotModel import RobotModel
from RobotCode.BehaviorModel import getBehaviorModel
import Server.WebApp as WebApp
import threading

cWorkingFolder = os.getcwd()
cRepoPath = os.path.dirname(os.path.abspath(__file__))
cRobotConfigurationPath = "./config/Robot_DarkPaw.json"

gRobot = None
def getRobot():
  global gRobot
  if None == gRobot:
    gRobot = RobotModel()
    gRobot.loadConfig(cRobotConfigurationPath)

    wBehaviorModel = getBehaviorModel()
    print(wBehaviorModel.getBehaviorMenu())
    wBehaviorModel.selectBehavior("Light", "TestLights")
    gRobot.setBehaviorManager(getBehaviorModel())
  return gRobot


def robotThread():
  wRobot = getRobot()
  try:
    print("Starting DarkPaw")
    wRobot.wake()
  except Exception as e:
    print(e)
    wRobot.sleep()
    

def WebAppThread():
  WebApp.subscribeToKillProcessCallback(ShutdownRoutine)
  WebApp.startWebApp(5000)


def ShutdownRoutine():
  wRobot = getRobot()
  wRobot.sleep()

  print("Changing working directory to [{}]".format(cWorkingFolder) )
  os.chdir(cWorkingFolder)

  print("Shutdown complete")


def main():

  print("Changing working directory to [{}]".format(cRepoPath) )
  os.chdir(cRepoPath)

  wThreadList = []
  wThreadList.append(threading.Thread(target=robotThread))
  wThreadList.append(threading.Thread(target=WebAppThread))

  try:
    for wThread in wThreadList:
      wThread.isDaemon = True
      wThread.start()

    for wThread in wThreadList:
      wThread.join()

  except Exception as e:
    print(e)
  ShutdownRoutine()
  return 0


if __name__ == '__main__':
  main()
