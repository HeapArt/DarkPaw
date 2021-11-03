import json
from os import wait
import time
import math

from .HWIO.LED import LED
from .HWIO.Switch import Switch

class RobotModel:
    def __init__(self):
        
        self._frequency = 25
        self._elaspTime = 0.0
            
        self._led_left = []
        self._led_right = []
        self._led_Controller = None

        self._switch_state = []
        self._switch_Controller = None
        return

    def cleanConfig(self):
        
        self._led_left = []
        self._led_right = []
        
        if None != self._led_Controller:
            del self._led_Controller
            self._led_Controller = None

        self._switch_state = []

        if None != self._switch_Controller:
            del self._switch_Controller
            self._switch_Controller = None

        return


    def loadConfig(self, iConfigJsonFilePath):
        wConfigObj = None
        try:
            with open(iConfigJsonFilePath, "r") as wConfigFile:
                wConfigObj = json.load(wConfigFile)
        except Exception as e:
            print("Robot Configuration Parsing Error [{}]".format(iConfigJsonFilePath))
            if None != e:
                print(e)
            return False

        self.cleanConfig()

        # Extract Robot Frequency
        if "Operating Frequency Hz" in wConfigObj:
            wFrequency = int (wConfigObj["Operating Frequency Hz"])
            if wFrequency < 1:
                wFrequency = 1
            self._frequency = wFrequency

        # Extract LED Mapping
        if "LED" in wConfigObj:
            self._led_Controller = LED()
            wLedConf = wConfigObj["LED"]
            if "left" in wLedConf:
                for wIndex in wLedConf["left"]:
                    wI = int(wIndex)
                    if wI >= 0:
                        self._led_left.append([wI,0,0,0]) 
            
            if "right" in wLedConf:
                for wIndex in wLedConf["right"]:
                    wI = int(wIndex)
                    if wI >= 0:
                        self._led_right.append([wI,0,0,0]) 
        
        # Extract Switch Mapping
        if "Switch GPIO" in wConfigObj:
            wPinArray = []
            self._switch_state = []
            for wPin in wConfigObj["Switch GPIO"]:
                print(wPin)
                if wPin > 0:
                    wPinArray.append(int(wPin))
                    self._switch_state.append(False)

            self._switch_Controller = Switch(wPinArray)
            

        print(self._switch_state)
        return False


    def wake(self):
        self.setLEDWipe_Left(iRed=255)
        self.update_LED()
        time.sleep(0.5)
        self.setLEDWipe_Left(iGreen=255)
        self.update_LED()
        time.sleep(0.5)
        self.setLEDWipe_Left(iBlue=255)
        self.update_LED()
        time.sleep(0.5)
        self.setLEDWipe_Left()
    

        self.setLEDWipe_Right(iRed=255)
        self.update_LED()
        time.sleep(0.5)
        self.setLEDWipe_Right(iGreen=255)
        self.update_LED()
        time.sleep(0.5)
        self.setLEDWipe_Right(iBlue=255)
        self.update_LED()
        time.sleep(0.5)
        self.setLEDWipe_Right()
        self.update_LED()
        time.sleep(0.5)
    
        for i in range(0, len(self._led_left)):
            self.setLEDWipe_Left()
            self.setLED_Left(i,255,255,255)
            self.update_LED()
            time.sleep(0.5)
    
        for i in range(0, len(self._led_right)):
            self.setLEDWipe_Right()
            self.setLED_Right(i,255,255,255)
            self.update_LED()
            time.sleep(0.5)
    
        self.setLEDWipe_Left()
        self.setLEDWipe_Right()
        return


    def run(self):
        if self._frequency < 1:
            self._frequency = 1

        wTimeStep = 1/self._frequency

        wLastDt0 = time.time() - wTimeStep
        while True:        
            wt0 = time.time()
            wDt = wt0 - wLastDt0
            wLastDt0 = wt0

            self._elaspTime = self._elaspTime + wDt
            self._tick(wDt, self._elaspTime)

            wt1 = time.time()
            wProcDt = wt1 - wt0
            wSlpT = wTimeStep - wProcDt
            if wSlpT > 0:
                time.sleep(wSlpT)
        
        return

    def sleep(self):
        self._led_Controller.colorWipe(0,0,0)
        print("Robot Terminate")
        return

    def _tick(self, iDt, iElapseTime):

        for i in range(0, len(self._led_left)):
            wWave = int(0.5*(math.sin(2*iElapseTime/math.pi + i*math.pi/18)+1)*255)
            self.setLED_Left(i,iBlue = wWave)
            self.setLED_Right(i,iBlue = wWave)
    
        self.update_LED()
        self.update_Switchs()
        return


    def update_LED(self):
        if None != self._led_Controller:
            self._led_Controller.setColorSet(self._led_left)
            self._led_Controller.setColorSet(self._led_right)
        return


    def update_Switchs(self):
        if None != self._switch_Controller:
            for wi in range(0, len(self._switch_state)):
                self._switch_Controller.switch(wi, self._switch_state[wi])
        return


    def setLED_Left(self, iIndex, iRed = 0, iGreen = 0, iBlue = 0):
        if iIndex >= 0:
            wPixel = self._led_left[iIndex%len(self._led_left)]
            wPixel[1] = iRed
            wPixel[2] = iGreen
            wPixel[3] = iBlue
        return


    def setLEDWipe_Left(self, iRed = 0, iGreen = 0, iBlue = 0):
        for wPixel in self._led_left:
            wPixel[1] = iRed
            wPixel[2] = iGreen
            wPixel[3] = iBlue
        return


    def setLED_Right(self, iIndex, iRed = 0, iGreen = 0, iBlue = 0):
        if iIndex >= 0:
            wPixel = self._led_right[iIndex%len(self._led_right)]
            wPixel[1] = iRed
            wPixel[2] = iGreen
            wPixel[3] = iBlue
        return


    def setLEDWipe_Right(self, iRed = 0, iGreen = 0, iBlue = 0):
        for wPixel in self._led_right:
            wPixel[1] = iRed
            wPixel[2] = iGreen
            wPixel[3] = iBlue
        return


    def setSwitch(self, iIndex, iOn = False):
        if iIndex > 0:
            self._switch_state[iIndex % len(self._switch_state)] = iOn
        return