#!/usr/bin/python

#sample solution for operation of the 'Boomer' robot produced by 
# Midlands STEMbotics robotics club in Winnsboro SC.
#Copyright (c) 2019 Midlands STEMbotics robotics club, Winnsboro South Carolina

import cwiid
import time
import gpiozero

#set up harware links for the two motors using the indicated GPIOS.
#NOTE: if SPI is active, must swap GPIO 20 to a different pin.
boomer = gpiozero.Robot(left=(27,17), right=(26,13))

#controller initialization
print("Press and hold the 1 + 2 buttons on the WII remote at the same time:")
time.sleep(5)
wii = cwiid.Wiimote()
print("Connection with remote established")
wii.rpt_mode= cwiid.RPT_BTN


#main command loop
while True:
    
    button_status = wii.state["buttons"]

    if(button_status & cwiid.BTN_UP):
        print("up button pressed")
        boomer.forward(0.3)
        time.sleep(0.2)
        continue

    elif(button_status & cwiid.BTN_DOWN):
        print("down button pressed")
        boomer.backward(0.3)
        time.sleep(0.2)
        continue

    elif(button_status & cwiid.BTN_RIGHT):
        print("right button pressed")
        boomer.right(0.3)
        time.sleep(0.2)
        continue

    elif(button_status & cwiid.BTN_LEFT):
        print("left button pressed")
        boomer.left(0.3)
        time.sleep(0.2)
        continue
    elif(button_status - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print("\nClosing connection ...")
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        exit(wii)
        break

