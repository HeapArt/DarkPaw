#! /usr/bin/python3
import os
import subprocess

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
  wRepoPath = os.path.dirname(os.path.realpath(__file__))
  wStartUpScriptPath = os.path.join(wRepoPath, "startup.sh")

  print("Creating start up script [{}]".format(wStartUpScriptPath))
	
  os.system('sudo -u {} touch {}'.format(os.getlogin(),wStartUpScriptPath))

  with open( wStartUpScriptPath,'w') as wScript:
    wScript.write("#! /bin/sh \n\
# wait a few seconds for Hardware to initialize\n\
/bin/sleep 10 \n\
# Execute DarkPaw Program\n\
sudo {}/DarkPawStart.py \n\
".format(wRepoPath))

  os.system('sudo chmod +x {}'.format(wStartUpScriptPath))

  wCronTabOut = subprocess.check_output(["sudo", "crontab", "-l" ])
  wCronTabOut = wCronTabOut.decode("utf-8").split('\n')
  
  wCronTabEntry = "@reboot sudo {}".format(wStartUpScriptPath)
  
  # check if startupscript is in crontab
  
  wFoundEntry = False
  for wLine in wCronTabOut:
    if wLine == wCronTabEntry:
      wFoundEntry = True
      break

  # add start up script to crontab
  if False == wFoundEntry:
    os.system("echo \"$(echo '{}' ; crontab -l 2>&1)\" | crontab -".format(wCronTabEntry))
        
  print("Startup File creation complete")

if __name__ == '__main__':
  installPythonRequirements()
  updateRPiConfigFile()
  createStartScript()
  print("Installion Commplete")
  #print('restarting...')
  #os.system("sudo reboot")
