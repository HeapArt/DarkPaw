
#def t1():
#  import pygame
#  pygame.mixer.init()
#  pygame.mixer.music.load("/home/pi/Downloads/test.mp3")
#  pygame.mixer.music.play()
#  while pygame.mixer.music.get_busy() == True:
#    continue

import time
from gtts import gTTS
import pygame 

def t2():
  
  tts = gTTS("Hello world the j")
  tts.save("hello.mp3")

  pygame.mixer.init()
  pygame.mixer.music.load("hello.mp3")
  pygame.mixer.music.play(1)
  while pygame.mixer.music.get_busy() == True:
    continue


if __name__ == '__main__':
    t2()