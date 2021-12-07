#!/usr/bin/python3
# File name   : LED.py
# Description : WS_2812
# Website     : based on the code from https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py
# Author      : original code by Tony DiCola (tony@tonydicola.com)
# Date        : 2019/02/23
import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LEDController:
    def __init__(self):
        self.LED_COUNT      = 16      # Number of LED pixels.
        self.LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        args = parser.parse_args()

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(R,G,B)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
            

    # Define functions which animate LEDs in various ways.
    def colorWipeSet(self, iPixelSet, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(R,G,B)
        for i in iPixelSet:
            if i >= 0:
                self.strip.setPixelColor(i, color)
        self.strip.show()
            

    def setColor(self, iPixel, R,G, B):
        color = Color(R, G, B)
        if iPixel >= 0:
            self.strip.setPixelColor(iPixel, color)
        self.strip.show()


    def setColorSet(self, iPixelSetWithColor):
        for wPixelWColor in iPixelSetWithColor:
            if wPixelWColor[0] >= 0:
                color = Color(wPixelWColor[1], wPixelWColor[2], wPixelWColor[3])
                self.strip.setPixelColor(wPixelWColor[0], color)
        self.strip.show()


def originalFunc():
    led = LEDController()
    try:  
        while True:  
            led.colorWipe(255, 0, 0)  # red
            time.sleep(1)  
            led.colorWipe(0, 255, 0)  # green
            time.sleep(1)  
            led.colorWipe(0, 0, 255)  # blue
            time.sleep(1) 
    except:  
        led.colorWipe(0,0,0)  # Lights out

def testFunc():
    led = LEDController()
    try:
        print("number of pixels are [{}]".format(led.strip.numPixels()))
        wCount = led.strip.numPixels()
        
        iPixel = 0
        i = 0
        inc = 5
        while True:
            if i <= 0:
                inc = 51
            elif i >= 255:
                inc = -51
            i = i + inc
            iPixel = iPixel+1
#            led.setColor(0, i,0,0)
#            led.setColor(1, 0,i,0)
#            led.setColor(2, 0,0,i)
#            led.setColor(3, i,i,0)
#            led.setColor(4, 0,i,i)
#            led.setColor(5, i,0,i)
            print(i)
            led.setColor(iPixel%6, i%255,(i+100)%255,(i+100)%255)
            time.sleep(0.25) 
            led.setColor(iPixel%6, 0,0,0)


    except:
        led.colorWipe(0,0,0)  # Lights out
        
        
if __name__ == '__main__':
    #testFunc()
    originalFunc()