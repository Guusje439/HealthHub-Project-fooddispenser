from machine import Pin, Timer

import A4988
from A4988 import MotorDriver

button1 = Pin(5, Pin.IN, Pin.PULL_UP) # Green Button
button2 = Pin(6, Pin.IN, Pin.PULL_UP) # Red Button

lock = False
timer1 = None # Timer for button reset
timer2 = None # Timer for the button cooldown

MOTOR_SPEED = 1000

def unlock(_):
    global lock
    lock = False

def stop(_):
    global motor
    global lock
    global timer2
    lock = True

    if timer2 is None:
        timer2 = Timer(mode=Timer.ONE_SHOT, period=1000, callback=unlock)
    else:
        timer2.init(mode=Timer.ONE_SHOT, period=1000, callback=unlock)
    motor.stop_motor()

if __name__ == "__main__":
    motor = MotorDriver(direction_pin=16, step_pin=17, steps_per_revolution=200)
    button2.irq(trigger=Pin.IRQ_RISING, handler=stop)
    motor.set_direction(A4988.DIR_CW)

    while True:
        if button1.value() == 0 and not lock:
            if timer1 is None:
                timer1 = Timer(mode=Timer.ONE_SHOT, period=5000, callback=stop)
            else:
                timer1.init(mode=Timer.ONE_SHOT, period=5000, callback=stop)
            motor.start_motor(MOTOR_SPEED)
            lock = True