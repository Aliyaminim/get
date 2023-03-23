import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.IN)

GPIO.output(22, GPIO.input(18))
time.sleep(10)
GPIO.output(22, 0)

