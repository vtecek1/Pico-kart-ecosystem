import time
import machine # type: ignore
from machine import ADC # type: ignore
import utime # type: ignore
 

 
mode = 'fsddrag'
brake = True
throttleInput = 10

while True:
    
    adc = ADC(19)
    throttleInput = adc.read_uv()
    print(throttleInput)
    
    
    while mode == 'drag':
        if throttleInput >= 10 and brake == True:
            throttleOutput = 25
        elif throttleInput >= 10:
            throttleOutput = 100
        else:
            throttleOutput = 0
        #print(throttleOutput)
        
    while mode == 'race':
        if throttleInput > 90:
            throttleOutput = 100
        elif throttleInput >= 10:
            throttleOutput = throttleInput*1.1
        else:
            throttleOutput = 0
        
    while mode == 'eco':
        previous = throttleInput
        time.sleep(0.3)
        throttleOutput = (previous + throttleInput)/2   
        print('Throttle In: ' + throttleInput + 'Throttle In: ' + throttleOutput)