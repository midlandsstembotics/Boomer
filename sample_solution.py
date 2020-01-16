#!/usr/bin/python

"""sample solution for operation of the 'Boomer' robot produced by Midlands STEMbotics robotics club in Winnsboro SC.

Copyright (c) 2019 Daniel E Campbell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


###################
gpiozero.robot class demo code
###################

class Robot(SourceMixin, CompositeDevice):
    
    Extends :class:`CompositeDevice` to represent a generic dual-motor robot.
    This class is constructed with two tuples representing the forward and
    backward pins of the left and right controllers respectively. For example,
    if the left motor's controller is connected to GPIOs 4 and 14, while the
    right motor's controller is connected to GPIOs 17 and 18 then the following
    example will drive the robot forward::

        from gpiozero import Robot
        robot = Robot(left=(4, 14), right=(17, 18))
        robot.forward()
    :param tuple left:
        A tuple of two (or three) GPIO pins representing the forward and
        backward inputs of the left motor's controller. Use three pins if your
        motor controller requires an enable pin.
    :param tuple right:
        A tuple of two (or three) GPIO pins representing the forward and
        backward inputs of the right motor's controller. Use three pins if your
        motor controller requires an enable pin.
    :param bool pwm:
        If :data:`True` (the default), construct :class:`PWMOutputDevice`
        instances for the motor controller pins, allowing both direction and
        variable speed control. If :data:`False`, construct
        :class:`DigitalOutputDevice` instances, allowing only direction
        control.
    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).
    .. attribute:: left_motor
        The :class:`Motor` on the left of the robot.
    .. attribute:: right_motor
        The :class:`Motor` on the right of the robot.
    

    def __init__(self, left=None, right=None, pwm=True, pin_factory=None, *args):
        # *args is a hack to ensure a useful message is shown when pins are
        # supplied as sequential positional arguments e.g. 2, 3, 4, 5
        if not isinstance(left, tuple) or not isinstance(right, tuple):
            raise GPIOPinMissing('left and right motor pins must be given as '
                                 'tuples')
        super(Robot, self).__init__(
            left_motor=Motor(*left, pwm=pwm, pin_factory=pin_factory),
            right_motor=Motor(*right, pwm=pwm, pin_factory=pin_factory),
            _order=('left_motor', 'right_motor'),
            pin_factory=pin_factory
        )

    @property
    def value(self):
        
        Represents the motion of the robot as a tuple of (left_motor_speed,
        right_motor_speed) with ``(-1, -1)`` representing full speed backwards,
        ``(1, 1)`` representing full speed forwards, and ``(0, 0)``
        representing stopped.
        
        return super(Robot, self).value

    @value.setter
    def value(self, value):
        self.left_motor.value, self.right_motor.value = value

    def forward(self, speed=1, **kwargs):
        
        Drive the robot forward by running both motors forward.
        :param float speed:
            Speed at which to drive the motors, as a value between 0 (stopped)
            and 1 (full speed). The default is 1.
        :param float curve_left:
            The amount to curve left while moving forwards, by driving the
            left motor at a slower speed. Maximum *curve_left* is 1, the
            default is 0 (no curve). This parameter can only be specified as a
            keyword parameter, and is mutually exclusive with *curve_right*.
        :param float curve_right:
            The amount to curve right while moving forwards, by driving the
            right motor at a slower speed. Maximum *curve_right* is 1, the
            default is 0 (no curve). This parameter can only be specified as a
            keyword parameter, and is mutually exclusive with *curve_left*.
        
        curve_left = kwargs.pop('curve_left', 0)
        curve_right = kwargs.pop('curve_right', 0)
        if kwargs:
            raise TypeError('unexpected argument %s' % kwargs.popitem()[0])
        if not 0 <= curve_left <= 1:
            raise ValueError('curve_left must be between 0 and 1')
        if not 0 <= curve_right <= 1:
            raise ValueError('curve_right must be between 0 and 1')
        if curve_left != 0 and curve_right != 0:
            raise ValueError("curve_left and curve_right can't be used at "
                             "the same time")
        self.left_motor.forward(speed * (1 - curve_left))
        self.right_motor.forward(speed * (1 - curve_right))

    def backward(self, speed=1, **kwargs):
        
        Drive the robot backward by running both motors backward.
        :param float speed:
            Speed at which to drive the motors, as a value between 0 (stopped)
            and 1 (full speed). The default is 1.
        :param float curve_left:
            The amount to curve left while moving backwards, by driving the
            left motor at a slower speed. Maximum *curve_left* is 1, the
            default is 0 (no curve). This parameter can only be specified as a
            keyword parameter, and is mutually exclusive with *curve_right*.
        :param float curve_right:
            The amount to curve right while moving backwards, by driving the
            right motor at a slower speed. Maximum *curve_right* is 1, the
            default is 0 (no curve). This parameter can only be specified as a
            keyword parameter, and is mutually exclusive with *curve_left*.
        
        curve_left = kwargs.pop('curve_left', 0)
        curve_right = kwargs.pop('curve_right', 0)
        if kwargs:
            raise TypeError('unexpected argument %s' % kwargs.popitem()[0])
        if not 0 <= curve_left <= 1:
            raise ValueError('curve_left must be between 0 and 1')
        if not 0 <= curve_right <= 1:
            raise ValueError('curve_right must be between 0 and 1')
        if curve_left != 0 and curve_right != 0:
            raise ValueError("curve_left and curve_right can't be used at "
                             "the same time")
        self.left_motor.backward(speed * (1 - curve_left))
        self.right_motor.backward(speed * (1 - curve_right))

    def left(self, speed=1):
        
        Make the robot turn left by running the right motor forward and left
        motor backward.
        :param float speed:
            Speed at which to drive the motors, as a value between 0 (stopped)
            and 1 (full speed). The default is 1.
        
        self.right_motor.forward(speed)
        self.left_motor.backward(speed)

    def right(self, speed=1):
        
        Make the robot turn right by running the left motor forward and right
        motor backward.
        :param float speed:
            Speed at which to drive the motors, as a value between 0 (stopped)
            and 1 (full speed). The default is 1.
        
        self.left_motor.forward(speed)
        self.right_motor.backward(speed)

    def reverse(self):
        
        Reverse the robot's current motor directions. If the robot is currently
        running full speed forward, it will run full speed backward. If the
        robot is turning left at half-speed, it will turn right at half-speed.
        If the robot is currently stopped it will remain stopped.
        
        self.left_motor.reverse()
        self.right_motor.reverse()

    def stop(self):
        
        Stop the robot.
        
        self.left_motor.stop()
        self.right_motor.stop()

#################
cwiid demo code
#################

import cwiid
import time
 
button_delay = 0.1
 
print 'Press 1 + 2 on your Wii Remote now ...'
time.sleep(1)
 
# Connect to the Wii Remote. If it times out
# then quit.
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Error opening wiimote connection"
  quit()
 
print 'Wii Remote connected...\n'
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'
 
wii.rpt_mode = cwiid.RPT_BTN
 
while True:
 
  buttons = wii.state['buttons']
 
  # If Plus and Minus buttons pressed
  # together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print '\nClosing connection ...'
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)
 
  # Check if other buttons are pressed by
  # doing a bitwise AND of the buttons number
  # and the predefined constant for that button.
  if (buttons & cwiid.BTN_LEFT):
    print 'Left pressed'
    time.sleep(button_delay)
 
  if(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_UP):
    print 'Up pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_A):
    print 'Button A pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_B):
    print 'Button B pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_HOME):

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
        continue

    elif(button_status & cwiid.BTN_DOWN):
        boomer.reverse(0.3)
        continue

    elif(buttons & cwiid.BTN_RIGHT):
        boomer.right(0.5)
        continue

    elif(buttons & cwiid.BTN_LEFT):
        boomer.left(0.5)
        continue
    else(buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print '\nClosing connection ...'
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        exit(wii)
        break
    
