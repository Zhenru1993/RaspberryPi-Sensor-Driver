import RPi.GPIO as GPIO
import time

# specified based on rasp pin connection
M_pin = 18 #motion orange

# return value is True/False
class MotionSensor:
    
    def __init__(self):
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BCM)
        GPIO.setup(M_pin,GPIO.IN)

    def read(self):
        for i in range(101):
            if GPIO.input(M_pin):
                return True
            else:
                return False
