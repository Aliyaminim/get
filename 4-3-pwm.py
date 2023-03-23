import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

p = GPIO.PWM(24, 0.1)
m = GPIO.PWM(22, 0.1)
p.start(0)
m.start(0)
try:
    while(True):
        a = input('input k ')
        p.start(int(a))
        m.start(int(a))
        input('press return to stop')
        p.stop()
        m.stop()
finally:
    GPIO.output(22, 0)
    GPIO.cleanup()