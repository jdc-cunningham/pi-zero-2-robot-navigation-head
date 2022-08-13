### Need to get this

Has info here
https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

Damn 1500 is midpoint but it can go to 40000 wtf

https://abyz.me.uk/rpi/pigpio/python.html

no it caps out at 2500 hmm

08/13/2022 9:31 AM

Learning this, reading the teachmemicro page above

arm position depends on the width of the pulse

duty cycle and frequency

1.5ms = 500 Hz and 75% duty cycle (75% of 2 is 1.5)

oh... I see (looking at their 1/500 2ms figure)

I am using `pi.set_servo_pulsewidth(GPIO_PIN, microseconds)`

1500 micro = 1.5 ms

damn...

there are these other commands to use

pi.set_PWM_frequency(#, #)
pi.set_PWM_dutycycle(#, #)
pi.set_PWM_range(#, #) // could be useful for min/max

https://electronics.stackexchange.com/questions/344026/controlling-the-speed-of-servo

Well I'm not really learning PWM, it seems you don't really control the speed of the servo

You can slow it down by slowly applying the pulsewidth time in increments

The thing is I'm not sure of units to use yet

Oh... the other issue is I don't have a starting position to base it off of the increments...

so on startup it will be fast unless it's near/at the position already

nice info here

https://resources.pcb.cadence.com/blog/2020-pulse-width-modulation-characteristics-and-the-effects-of-frequency-and-duty-cycle

servo anticipates an update every 20ms
pulse between 1 and 2 ms

duty cycle of 5% to 10% at 50hz

1.5ms as mentioned above is middle

oh duty cycle is about how much of it is on vs. off, 50% means half on half off (wave)

one quarter in off state means 75% on state

frequency needs to be high enough to not affect load

interesting info about PWM frequency electric part being more than mechanical

https://gearsmagazine.com/magazine/exploring-pwm-frequency-and-duty-cycle/

well... I don't really understand this, I know enough to do what I want to do eg. "slow down" the servo
