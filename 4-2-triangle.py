import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [10, 9, 11, 5, 6, 13, 19, 26]
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    while(True):
        t = input('enter time ')
        time_sleep = int(t)/256/2
        for i in range(256):
            GPIO.output(dac, decimal2binary(i))
            time.sleep(time_sleep)
        for i in range(255, -1, -1):
            GPIO.output(dac, decimal2binary(i))
            time.sleep(time_sleep)
except KeyboardInterrupt:
        print('stopped')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
