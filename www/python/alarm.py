from sense_hat import SenseHat
from playsound import playsound
import datetime
import time

sense = SenseHat()
sense.rotation = 180


x = datetime.datetime.now()

print("Current time:", x.strftime("%H"), ":" ,x.strftime("%M"))
