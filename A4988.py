from machine import Pin, Timer
import utime

DIR_CCW = 0
DIR_CW  = 1

led = Pin(25, Pin.OUT)

class MotorDriver:
	def __init__(self, direction_pin: int, step_pin: int, steps_per_revolution: int):
		self.direction_pin = Pin(direction_pin, Pin.OUT)
		self.step_pin = Pin(step_pin, Pin.OUT)
		self.steps_per_revolution = steps_per_revolution
		self.motor_timer = Timer()

	def __del__(self):
		self.motor_timer.deinit()

	def set_direction(self, direction: int):
		self.direction_pin.value(direction)

	def step(self, steps: int):
		for _ in range(steps):
			self.step_pin.value(not self.step_pin.value())

	def start_motor(self, speed: int):
		self.motor_timer.init(freq=1000000 // speed, mode=Timer.PERIODIC, callback=lambda timer: self.step(1))
		led.on()
		utime.sleep_ms(self.steps_per_revolution)

	def stop_motor(self):
		self.motor_timer.deinit()
		led.off()
