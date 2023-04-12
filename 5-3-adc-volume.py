import RPi.GPIO as GPIO
import time

dac = [10, 9, 11, 5, 6, 13, 19, 26]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
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
GPIO.setup(leds, GPIO.OUT)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    signal = num2dac(0)
    res = 0
    for value in range(8):
        signal[value] = 1
        GPIO.output(dac, signal)
        time.sleep(0.005)
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 0:
            signal[value] = 0
        else:
            signal[value] = 1
            res += 2**(7 - value)
    return res 

  
try:
    while (True):
        res = adc()
        kol = round(res/255*8) 
        leds_l = decimal2binary(0)
        for i in range(kol):
            leds_l[7-i] = 1
        GPIO.output(leds,leds_l)
except KeyboardInterrupt:
    print('\nThe program was stopped by the Keyboard')
finally:
    GPIO.output(dac, 0)
    GPIO.output(comp, 0)
    GPIO.cleanup()