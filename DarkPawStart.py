import os
from RobotCode.RobotModel import RobotModel

cRobotConfigurationPath = "./config/Robot_DarkPaw.json"

def main():
    wWorkingFolder = os.getcwd()
    wRepoPath = os.path.dirname(os.path.abspath(__file__))

    print("Changing working directory to [{}]".format(wRepoPath) )
    os.chdir(wRepoPath)

    wRobot = RobotModel()
    wRobot.loadConfig(cRobotConfigurationPath)
    
    try:
        print("Starting DarkPaw")
        wRobot.wake()
        wRobot.run()
    except Exception as e:
        print(e)

    print("Shutting down DarkPaw")
    wRobot.sleep()
    print("Shutdown complete")

    print("Changing working directory to [{}]".format(wWorkingFolder) )
    os.chdir(wWorkingFolder)
    return 0


if __name__ == '__main__':
    main()
