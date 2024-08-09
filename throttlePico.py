import time
import machine # type: ignore
from machine import ADC # type: ignore
import utime # type: ignore
 


mode = 'fsddrag'
brake = True
throttleInput = 10

while True:
    
    adc = ADC(27)
    throttleInput = adc.read_uv()
    print(throttleInput)
    adc_out = ADC(26)
    pwm = machine.PWM(adc_out)
    
    if  machine.pin(2) == '1':
        mode = 'drag'
    elif  machine.pin(3) == '1':
        mode = 'race'
    elif  machine.pin(4) == '1':
        mode = 'eco'
    
    while mode == 'drag':
        if throttleInput >= 10 and brake == True:
            throttleOutput = 25
        elif throttleInput >= 10:
            throttleOutput = 100
        else:
            throttleOutput = 0
        #print(throttleOutput)
        
        pwm.freq(500)
        pwm.duty((1024/100)*throttleOutput)
        
    while mode == 'race':
        if throttleInput > 90:
            throttleOutput = 100
        elif throttleInput >= 10:
            throttleOutput = throttleInput*1.1
        else:
            throttleOutput = 0
            
        pwm.freq(500)
        pwm.duty((1024/100)*throttleOutput)
        
    while mode == 'eco':
        previous = throttleInput
        time.sleep(0.3)
        throttleOutput = (previous + throttleInput)/2   
        print('Throttle In: ' + throttleInput + 'Throttle In: ' + throttleOutput)
        
        pwm.freq(500)
        pwm.duty((1024/100)*throttleOutput)