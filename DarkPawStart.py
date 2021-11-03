import os
from RobotCode.RobotModel import RobotModel
from Server.WebApp import startWebApp
import threading

cRobotConfigurationPath = "./config/Robot_DarkPaw.json"


def robotThread(iRobot):
    try:
        print("Starting DarkPaw")
        iRobot.wake()
        iRobot.run()
    except Exception as e:
        print(e)
    
    print("Shutting down DarkPaw")
    iRobot.sleep()
    

def WebAppThread(iRobot):
    startWebApp(5000)

def main():
    wWorkingFolder = os.getcwd()
    wRepoPath = os.path.dirname(os.path.abspath(__file__))

    print("Changing working directory to [{}]".format(wRepoPath) )
    os.chdir(wRepoPath)

    wRobot = RobotModel()
    wRobot.loadConfig(cRobotConfigurationPath)
    
    wThreadList = []
    wThreadList.append(threading.Thread(target=robotThread,  args=(wRobot,)))
    wThreadList.append(threading.Thread(target=WebAppThread, args=(wRobot,)))

    for wThread in wThreadList:
        wThread.isDaemon = True
        wThread.start()

    for wThread in wThreadList:
        wThread.join()

    print("Shutdown complete")

    print("Changing working directory to [{}]".format(wWorkingFolder) )
    os.chdir(wWorkingFolder)
    return 0


if __name__ == '__main__':
    main()
