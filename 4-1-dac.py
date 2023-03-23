import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
dac = [10, 9, 11, 5, 6, 13, 19, 26]
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


try:
    while (True):
        a = input('please input number 0-255 ')
        if a == 'q':
            sys.exit()
        elif a.isdigit() and float(a) == int(a) and 0 <= int(a) <= 255:
            GPIO.output(dac, decimal2binary(int(a))
            print("{:.2f}".format(int(a)*3.3/256))
        else:
            print('Please input number 0-255 again')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()