import RPi.GPIO as GPIO
import time
from matplotlib import pyplot

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(leds)
levels = 2 ** bits
maxVoltage = 3.3
comp = 4
troyka = 17
comparatorValue = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

#перевод в двоичную СО
def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

#отображение на светодиодах dac
def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

#снятие показаний с тройки
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
    results = []
    GPIO.setup(troyka, GPIO.OUT, initial=1)
    time_start = time.time()
    count = 0
    voltage = 0

    #зарядка конденсатора
    print('начинаем заряжать конденсатор')
    while voltage < 256*0.8:
        voltage = adc()
        results.append(voltage)
        time.sleep(0.001)
        count += 1
        GPIO.output(leds, decimal2binary(voltage))

    time_zar = time.time() - time_start
    GPIO.setup(troyka, GPIO.OUT, initial = 0)

    #разряжаем конденсатор
    print('разряжаем конденсатор')
    while voltage > 256*0.7:
        voltage = adc()
        results.append(voltage)
        time.sleep(0.001)
        count += 1
        GPIO.output(leds, decimal2binary(voltage))

    time_raz = time.time() -time_start - time_zar
    time_experiment = time.time() - time_start

    #записываем данные в файлы
    print('записываем данные в файлы')
    with open('data.txt', 'w') as f:
        for i in results:
            f.write(str(i) + '\n')

    with open('settings.txt', 'w') as f: 
        f.write(str(1/time_experiment/count) + '\n')
        f.write(str(3.3/256))

    print('общая продолжительность эксперимента {},  период одного измерения {}, средняя частота дискретизации проведённых измерений {}, шаг квантования АЦП {}'.format(time_experiment, time_experiment/count, 1/time_experiment/count, 0.013))


    #построим графики
    print('построим графики')
    y = [i/256*3.3 for i in results]
    x = [i*time_experiment/count for i in range(len(results))]

    pyplot.plot(x, y)
    pyplot.xlabel('время')  
    pyplot.ylabel('напряжение') 
    pyplot.show()  
        
    

except KeyboardInterrupt:
    print('\nThe program was stopped by the Keyboard')
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(comp, 0)
    GPIO.cleanup()
