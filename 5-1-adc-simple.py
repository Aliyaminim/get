import RPi.GPIO as GPIO
import time

dac = [10, 9, 11, 5, 6, 13, 19, 26]
bits = len(dac)
levels = 2 ** bits
maxVoltage = 3.3
comp = 4
troyka = 17
comparatorValue = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    for value in range(256):
        signal = num2dac(value)
        time.sleep(0.005)
        voltage = value/levels *maxVoltage
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 0:
            return value  
  
try:
    while (True):
        value = adc()
        print(value)
except KeyboardInterrupt:
    print('\nThe program was stopped by the Keyboard')
finally:
    GPIO.output(dac, 0)
    GPIO.output(comp, 0)
    GPIO.cleanup()