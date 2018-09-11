from sense_hat import SenseHat
import pygame
import datetime
import time

sense = SenseHat()
sense.rotation = 180

pygame.init()

x = datetime.datetime.now()

pygame.mixer.music.load('alarm.mp3')
pygame.mixer.music.play(1)
print("Current time:", x.strftime("%H"), ":" ,x.strftime("%M"))
