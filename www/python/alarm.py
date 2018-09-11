from sense_hat import SenseHat
import pygame
import datetime

# Initiate the sensehat and the 'sound engine'
sense = SenseHat()
pygame.init()

# Load the alarm sound
pygame.mixer.music.load('../resources/alarm.mp3')

# Get the current time and format it to hhmm
x = datetime.datetime.now()
currentTime = x.strftime("%H%M")

# The current alarm time in hhmm
wakeTime = "1337"

# While the current time matches the alarm time, play the alarm
# play(1) means play once, -1 means infinitely
while wakeTime == currentTime:
    pygame.mixer.music.play(1)
