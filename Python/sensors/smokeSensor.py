import RPi.GPIO as GPIO
import time

# need to be specified based on rasp pin connection
SPICLK = 2  #mq2 orange
SPIMISO = 3 #mq2 brown
SPIMOSI = 4 #mq2 purple
SPICS = 14 #mq2 blue
mq2_dpin = 15 #mq2 green
mq2_apin = 0

# This class to handle the data collection for smoke sensor
# read value is float
class SmokeSensor:
    def __init__(self):
        #GPIO.setwarnings(False)
        #GPIO.cleanup()			
        #GPIO.setmode(GPIO.BCM)	    
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)
        GPIO.setup(mq2_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  
        GPIO.output(cspin, False)     

        commandout = adcnum
        commandout |= 0x18  
        commandout <<= 3    
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

            adcout = 0
            for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                    adcout |= 0x1

            GPIO.output(cspin, True)
            
            adcout >>= 1
            return adcout

    def read(self):
        COlevel=self.readadc(mq2_apin,SPICLK,SPIMOSI,SPIMISO,SPICS)
        if GPIO.input(mq2_dpin):
            return None
        else:
            return ("%.2f"%((COlevel/1024.)*3.3))
