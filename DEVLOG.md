Friday 08/05/2022

7:36 PM

Well I rewired it, took me a bit

What I'm having a problem with now is the MPU6050 code is not working.

I see the IMU on the address bus but it keeps saying can't find it.

Everything else checks, still have to run the camera.

I also designed and printed out the bottom stand.

I'm reprinting the cross with some mods (bigger and stronger)

Ohh... a wire broke off interesting.

lol both wires were broken off when I bent it into place, nice

It might be interference, my wire is very long, it's 

8:40 PM

Well... for some reason that i2c port does not want to work

SDA to GND is at 0.9V or so not sure why

I retouched the GPIO pins no change

I'll touch it up one more time, but if nothing else I'll use the parallel wire method and use the same bus.

Yeah I'm gonna have to try and paralell bus wire hmm

Thursday 08/04/2022

Half ass sucks

Printed the entire thing, was hard to get the supports out, broke stuff.

Had to update design and reprint in parts, up the infil too.

Doing IMU first

This looks good
https://github.com/m-rtijn/mpu6050

Hmm gravity is not accurate it's below 9.8

It should be enough to do NED though

tof

using smbus2

modifying VL53L0X file

nvm same issue module not found ugh

7:17 PM
Got this working but there's an issue with the whole library imports... can only get my code to run in the folder of the library...

Not a huge deal I can probably just start that file as a thread/looping function and call into it as needed but yeah

ehh

Oh damn I got lucky, looks like Pi only has one uart port, or at least immediately available

also the concern mixing python2 and 3

I'll get this all sorted after I make all the methods callable

I still have to wire everything up

So far it seems things prefer to work with python3

lol no there's more than one serial `dtoverlay -a`

7:51 PM
having troubles interfacing with Lidar... script I usually use doesn't work

Holy crap this [tfmini-s library](https://github.com/budryerson/TFMini-Plus_python) is good

It makes the TFmini-s accurate as hell, like below 30cm

Wow

Oh crap this thing is for tfmini plus but somehow it works on the s

Well it does say in the readme it's compatible, that's great



Wednesday 08/03/2022

Back on it. Feeling like I have left over energy.

I'm trying out hardware pwm as described [here](https://abyz.me.uk/rpi/pigpio/python.html#hardware_PWM)

5:35 PM
I have this strong urge/feeling of not wanting to do this... just so much work.

But the end result will be cool.

8:23 PM

Damn that's gonna take about 6 hrs to print oof

I'll interface with electronics in the meantime

Monday 08/01/2022

Trying to do some work on this.

Printing the pan-tilt cross bracket thing

I'm trying to simplify the pan/tilt setup, and also print it in parts/assemble it

Should use less material/be faster to print and can be changed

6:42 PM

I feel so spent, trying to get motivated to do this

7:27 PM

I'm struggling... not really getting anywhere

9:12 PM

I'm concerned about the gear rotation not working, printed out a basic shaft to check

11:05 PM
Need to extend/add end caps just to make sure pegs stay in.

Needs inner bushings/stoppings as well

11:23 PM

The motion is not smooth with this servo driver, will have to look into others

Also the max range is capped to the 90 degrees but Arduino has it more than that eg. full 180 degrees

Sunday 07/31/2022

8:45 AM back at it

I've got my gears figured out. I need to finish designing the pan/tilt assembly, make it, fix some measurement issues then fully assemble the body.

Then add the basic electronics to the buggy that it will drive.

10:21 AM

Man this is slow. I did some cleaning earlier but that was only like 20 mins

Damn I'm losing steam, realizing how much time it will take to print stuff

11:05 AM

I need the power of the poompa (my playlist and headphones)

Drown myself in music to get through it

# YEAAAH YEAAAH YEAHHHH AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

(Scorpions Blackout)

11:29 AM

bearing press fit print test, too loose

11:45 AM

Once assembled, this thing will not be easy to charge. I just realized I will have to change the switch for a JST and then I'll disconect it to recharge it through the BMS.

I have actual chargers to use but I can't just pop the cell out.

12:05 PM

Screwing around with bearing fit, went inwards then outwards (undo) like for real

2:12 PM

Starting to print the big stuff, still designing sensor bed

4:26 PM

Damn... a 7hr print lol oof

Ahh man the sensor bed model is so bad... so many broken surfaces.

I think I'm going to have to dissect it and rebuild each sub part.

<img src="./problems.JPG" width="800"/>

Ugh... this peg support thing broke off and it's just dragging non supported plastic threads around hmm...

Thankfully I can save most of the print/still use it. It looks flimsy though.

Nope in the end it failed at 80% dang... just because of that one overhang/support that failed.

Anyway the base is too flimsy, need to redesign it.

Saturday 07/30/2022

9:39 AM

I just modeled the Pi Zero 2 W, I have more parts to do.

I'm concerned about driving the servos from the Pi, but maybe it will be okay.

Last time I used an Arduino board that talked to the Pi. I think I just need to put some pull up resistors on the servos to keep them calm on boot.

11:30 AM

The left/right sensors are 0.9" away from the camera lens midpoint

*Gloria... you're always on the run now...*

11:59 AM

Still don't have a pan-tilt design yet.

I modeled the servo arms because I'm going to end up cutting them, putting them as a slot in whatever gear set I design.

Because making 3D printed servo horn splines is not a great idea in my experience/level of accuracy.

I'm glad to be working in Python, it's easier than C++

2:06 PM

Damn... slow going, test printing gears to make sure they work well

2:13 PM

Losing steam... but will keep going.

3:53 PM

I'm kind of flailing right now.

I'm printing gears... realizing having one side it attaches to makes it tip that way hmm...

I'm going to mess around with the Pi Zero/test the servo motion.

4:29 PM

Not sure why I didn't decide to use the two-servo arm with two screws.

Using just one makes the gear dip one way/not be level. Also the screw heads are too close to the body sadly. So they have to come in from the other side, not much contact will use glue.

6:44 PM

Still stuck on the chaise longue (not showing up on wifi)

7:26 PM ahh man...

So I had to connect to an external monitor... I did some updates

I confirmed that the ip address was the one I thought it would be, it doesn't identify itself as a pi

Now I have SSH'd into it by my ASUS C100P Chromebook

Where I will write some servo test code.

8:04 PM

ran servo with Python using ASUS

problem with git though, concerned about degrees not going that far