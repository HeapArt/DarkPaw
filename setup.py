#!/usr/bin/python3
import os

def installPythonRequirements():
    # Install python requirements
    print("Installing Python requirments")
    os.system("sudo pip3 install -r requirements.txt")
    print("Complete Installation of Python requirments")

def updateRPiConfigFile():
    print("Configurating Raspberry Pi boot/config.txt")
    # Replace keys in boot/config.txt

    # Backup File
    print("Creating back up of /boot/config.txt at /boot/config.txt.back_up")
    os.system("sudo cp /boot/config.txt /boot/config.txt.back_up")

    # Defining keys
    wKeysToReplace = [
         ["#dtparam=i2c_arm=on", "dtparam=i2c_arm=on"]
        ,["dtparam=i2c_arm=off", "dtparam=i2c_arm=on"]
        ,["#dtparam=i2c_arm=off", "dtparam=i2c_arm=on"]
        ,["start_x=0", "start_x=1"]
        ,["#start_x=1", "start_x=1"]
        ,["#start_x=0", "start_x=1"]
    ]

    with open("/boot/config.txt.back_up", "r") as wCIn:
        with open("/boot/config.txt", "w") as wCOut:
            for wLine in wCIn:
                wModLine = wLine
                for wKey in wKeysToReplace:
                    wModLine = wModLine.replace(wKey[0], wKey[1])
                wCOut.write(wModLine)

    print("Complete configurating Raspberry Pi boot/config.txt")


def createStartScript():
    wRepoPath = "/" + os.path.dirname(os.path.realpath(__file__))
    wStartUpScriptPath = "//home/pi/startup.sh"

    print("Creating start up script [{}]".format(wStartUpScriptPath))
	
    os.system('sudo touch {}'.format(wStartUpScriptPath))

    with open( wStartUpScriptPath,'w') as wScript:
        wScript.write("#!/bin/sh\nsudo python3 {}/DarkPawStart.py".format(wRepoPath))

    os.system('sudo chmod 777 {}'.format(wStartUpScriptPath))

    # Backup File
    print("Creating back up of /etc/rc.local at /etc/rc.local.back_up")
    os.system("sudo cp /etc/rc.local /etc/rc.local.back_up")

    with open("/etc/rc.local.back_up", "r") as wCIn:
        with open("/etc/rc.local", "w") as wCOut:
            wCmd = "{} start".format(wStartUpScriptPath)
            wCmdAlreadyAdded = False
            wFileLines = wCIn.readlines()
            for wLine in wFileLines:
                if wLine == wCmd:
                    print("Command Found")
                    wCmdAlreadyAdded = True
            if False == wCmdAlreadyAdded:
                for wLine in wFileLines:
                    wCOut.write(wLine)
                    if 0 <= wLine.find("fi") and False == wCmdAlreadyAdded:
                        print("Printing Command")
                        wCOut.write(wCmd)
                        wCmdAlreadyAdded = True
                
    print("Startup File creation complete")

if __name__ == '__main__':
    installPythonRequirements()
    updateRPiConfigFile()
    createStartScript()
    print("Installion Commplete")
    #print('restarting...')
    #os.system("sudo reboot")
