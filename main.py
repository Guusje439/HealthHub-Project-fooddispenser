from machine import Pin, Timer
import time

button1 = Pin(5, Pin.IN, Pin.PULL_UP) # Green Button
button2 = Pin(6, Pin.IN, Pin.PULL_UP) # Red Button
led = Pin(25, Pin.OUT)

lock = False
timer1 = None # Timer for button reset
timer2 = None # Timer for the button cooldown

def unlock(_):
    global lock
    lock = False

def stop(_):
    global lock
    global timer2

    led.off()
    lock = True

    if timer2 is None:
        timer2 = Timer(mode=Timer.ONE_SHOT, period=1000, callback=unlock)
    else:
        timer2.init(mode=Timer.ONE_SHOT, period=1000, callback=unlock)

button2.irq(trigger=Pin.IRQ_RISING, handler=stop)

while True:
    if button1.value() == 0 and not lock:
        if timer1 is None:
            timer1 = Timer(mode=Timer.ONE_SHOT, period=5000, callback=stop)
        else:
            timer1.init(mode=Timer.ONE_SHOT, period=5000, callback=stop)
        led.on()
        lock = True