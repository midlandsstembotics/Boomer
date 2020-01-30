#!/usr/bin/python

"""sample solution for operation of the 'Boomer' robot produced by Midlands STEMbotics robotics club in Winnsboro SC.

Copyright (c) 2019 Midlands STEMbotics robotics club, Winnsboro South Carolina
"""



import cwiid
import time
import gpiozero

boomer = gpiozero.Robot(left=(X,y), right=(x,y))

#controller initialization
print("Press and hold the 1 + 2 buttons on the WII remote at the same time:")
time.sleep(2)
wii = cwiid.Wiimote()
print("Connection with remote established")
wii.rpt_mode= cwiid.RPT_BTN



#main command loop
while True:
    
    button_status = wii.state["buttons"]

    if(button_status & cwiid.BTN_UP):
        boomer.forward(0.5)
        print("up button pressed")
        continue

    elif(button_status & cwiid.BTN_DOWN):
        boomer.reverse(0.3)
        print("down button pressed")
        continue

    elif(buttons & cwiid.BTN_RIGHT):
        boomer.right(0.5)
        print("right button pressed")
        continue

    elif(buttons & cwiid.BTN_LEFT):
        boomer.left(0.5)
        print("left button pressed")
        continue
    elif(buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print("\nClosing connection ...")
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        exit(wii)
        break
    
