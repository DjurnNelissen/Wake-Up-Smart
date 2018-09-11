from sense_hat import SenseHat
import playsound
import datetime
import time

sense = SenseHat()
sense.rotation = 180


x = datetime.datetime.now()

print(x.strftime("%H")":"x.strftime("%M"))
