#include <Arduino.h>

#define BUTTON_PIN 13

int count = 0;
bool timerRunning = false;

void setup() {
	// Source: https://www.instructables.com/Arduino-Timer-Interrupts/
	cli(); //stop interrupts

	TCCR1A = 0; // set entire TCCR1A register to 0
	TCCR1B = 0; // same for TCCR1B
	TCNT1  = 0; //initialize counter value to 0
	// set compare match register for 1hz increments
	OCR1A = 15624; // = (16*10^6) / (1*1024) - 1 (must be <65536)
	// turn on CTC mode
	TCCR1B |= (1 << WGM12);
	// Set CS10 and CS12 bits for 1024 prescaler
	TCCR1B |= (1 << CS12) | (1 << CS10);

	sei(); //allow interrupts
}

void enableTimer() {
	// enable timer compare interrupt
	TIMSK1 |= (1 << OCIE1A);
	timerRunning = true;
}
void disableTimer() {
	// enable timer compare interrupt
	TIMSK1 &= ~(1 << OCIE1A);
	timerRunning = false;
}

void loop() {
	if (digitalRead(BUTTON_PIN) == HIGH && !timerRunning) {
		enableTimer();
		count = 0;
	}
}

// 1Hz timer interrupt
ISR(TIMER1_COMPA_vect) {
	if (count == 5) {
		// DO STUFF
		// Disable timer
		disableTimer();
	} else {
		count++;
	}
}
