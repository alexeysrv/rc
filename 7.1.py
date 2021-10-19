import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
L = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH) #подаём питание на тройку-модуль
t_start = time.time()
GPIO.setup(4, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
        value = 128
        for i in range(6, 0, -1):
            signal = bin2dac(value)
            time.sleep(0.0007)
            comparatorValue = GPIO.input(4)
            if comparatorValue == 0:
                value = value - 2**i
            elif comparatorValue == 1:
                value = value + 2**i   
        voltage = value / levels * maxVoltage
        signal = bin2dac(value)
        GPIO.output(leds, signal)
        time.sleep(0.01)
        #print("Entered value = {:^3}, analog votage = {:.2f}".format(value, voltage))
        return value     

            
    

try:
    value = adc()
    print("Началась зарядка конденсатора")
    while value < 250:      #зарядка конденсатора
        value = adc()
        L.append(value)
        print("Конденсатор заряжается осталось ", int((1 - value / 250) * 100), "%")
                
    GPIO.output(17, GPIO.LOW) 
    print("Конденсатор зарядился! \n Началась разрядка конценсатора ")
    while value > 2:        #разрядка конденсатора
        value = adc()
        L.append(value)
        print("Конденсатор разряжается осталось ", int((value / 250) * 100), "%")
    t_stop = time.time()
    timexp = t_stop - t_start
    fm = int(len(L) / timexp)
    step = maxVoltage / timexp
    T = timexp / len(L)
    print("Измерения завершены")
    print("Суммарное время измерений = ", timexp, "число измерений = ", len(L), "частота = ", fm)
    L_str = [str(item) for item in L]
    
    with open("data.txt", "w") as data:
        data.write("\n".join(L_str))
    with open("settings.txt", "w") as set:
        set.write("Суммарное время измерений = ")
        set.write(str(timexp))
        set.write("\n Период измерений = ")
        set.write(str(T))
        set.write("\n Шаг по напряжению = ")
        set.write(str(step))
    
    plt.plot(L)
    plt.show() 
    

      
finally:
    GPIO.output(17, GPIO.LOW)
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    print("GPIO cleanup completed")