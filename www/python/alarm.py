from sense_hat import SenseHat
import datetime
import common
import pygame

# Initiate the sensehat and the 'sound engine'
sense = SenseHat()
c = common.common()
pygame.init()

# Load the alarm sound
pygame.mixer.music.load('../resources/alarm.mp3')

# Get the current time and format it to hhmm
x = datetime.datetime.now()
currentTime = x.strftime("%H%M")

# The current alarm time in hhmm
alarmTime = c.get_alarmTime()

# While the current time matches the alarm time, play the alarm
# play(1) means play once, -1 means infinitely
while alarmTime == currentTime:
    pygame.mixer.music.play(1)
