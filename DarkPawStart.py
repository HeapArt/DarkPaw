import os
import threading

from RobotCode.RobotModel import getRobotModel
from RobotCode.RobotApi import Robot_Api_BluePrint
from Server import WebApp

cWorkingFolder = os.getcwd()
cRepoPath = os.path.dirname(os.path.abspath(__file__))
cRobotConfigurationPath = "./config/Robot_DarkPaw.json"

def robotThread():

  wRobot = getRobotModel()
  wRobot.loadConfig(cRobotConfigurationPath)
  wRobot.getBehavior().selectBehavior("LED", "Test LED")

  try:
    print("Starting DarkPaw")
    wRobot.wake()
  except Exception as e:
    print(e)
    wRobot.sleep()
    

def WebAppThread():
  WebApp.subscribeToKillProcessCallback(ShutdownRoutine)

  wBluePrintList = [Robot_Api_BluePrint]
  WebApp.startWebApp(5000, wBluePrintList)


def ShutdownRoutine():
  wRobot = getRobotModel()
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
