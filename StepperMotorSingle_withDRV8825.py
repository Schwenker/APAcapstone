import RPi.GPIO as gpio
import time
import sys

ms0 = 29
ms1 = 31
ms2 = 33
direction = 11
step = 13

gpio.setmode(gpio.BOARD) # BOARD mode means literal physical pin numbers
gpio.setup(direction, gpio.OUT) #direction
#gpio.setup(step, gpio.OUT) #step

#gpio.setup(ms0, gpio.OUT) #ms0
#gpio.setup(ms1, gpio.OUT) #ms1
#gpio.setup(ms2, gpio.OUT) #ms2

def set_stepper_on():
        gpio.output(step, 0)
        time.sleep(0.001)
        gpio.output(step, 1)
        time.sleep(0.001)
                   
#def set_cw():
#        gpio.output(direction, 0)

#def set_anticw():
#        gpio.output(direction, 1)

#def ms_steps():
#        gpio.output(ms0, 0)
#        gpio.output(ms1, 0)
#        gpio.output(ms2, 0)

#ms_steps()
#set_cw()

infinite_loop = True
steps=0
while (infinite_loop == True):
        set_stepper_on()
        steps+=1
        print (steps)

#GPIO.ceanup()