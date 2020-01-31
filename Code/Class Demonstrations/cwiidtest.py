#!/usr/bin/python3

"""Test of the CWIID python3 library used in the 'Boomer' robot produced 
    by Midlands STEMbotics robotics club in Winnsboro SC.
Copyright (c) 2019 Midlands STEMbotics robotics club, Winnsboro South Carolina
"""



import cwiid
import time
import gpiozero

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
        #time.sleep(0.1)
        continue

    elif(button_status & cwiid.BTN_DOWN):
        print("down button pressed")
        #time.sleep(0.1)
        continue

    elif(button_status & cwiid.BTN_RIGHT):
        print("right button pressed")
        #time.sleep(0.1)
        continue

    elif(button_status & cwiid.BTN_LEFT):
        print("left button pressed")
        #time.sleep(0.1)
        continue
    elif(button_status - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print("\nClosing connection ...")
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 1
        exit(wii)
        break
    
