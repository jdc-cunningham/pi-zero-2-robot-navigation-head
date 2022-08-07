### Sunday 08/07/2022

Figure [this out](https://raspberrypi.stackexchange.com/questions/97995/rpi-python-i2c-ioerror-errno-121-remote-i-o-error-problem-how-to-fix-it
)

Do something hard with fresh brain

Maybe design how the robot deals with state

Also figure out the commands based on degrees turned on wheeled robot and desired distance (circumference) confirm with reality

8:55 AM
Ahh fresh brain, what will I do today mmm.

So... this is interesting, the imu started working after I pulled out the ToF set.

Well actually I also have to unplug the LED and servos hmmm

I can get more lines but it's still unstable dang

```
{'x': -0.4165910888671875, 'y': -0.4381389038085937, 'z': 9.193734375}
{'x': -0.4572925170898437, 'y': -0.38786066894531246, 'z': 9.169792358398437}
{'x': -0.43574470214843747, 'y': -0.3902548706054687, 'z': 9.313444458007812}
{'x': -0.43574470214843747, 'y': -0.40940848388671874, 'z': 9.205705383300781}
{'x': -0.430956298828125, 'y': -0.3495534423828125, 'z': 9.212887988281249}
{'x': -0.43574470214843747, 'y': -0.430956298828125, 'z': 9.210493786621093}
{'x': -0.4644751220703125, 'y': -0.5195417602539062, 'z': 9.320627062988281}
{'x': -0.42377369384765623, 'y': -0.5003881469726562, 'z': 9.229647399902344}
{'x': -0.4572925170898437, 'y': -0.3902548706054687, 'z': 9.327809667968749}
{'x': -0.6105214233398437, 'y': -0.316034619140625, 'z': 9.239224206542968}
{'x': -0.47165772705078124, 'y': -0.41419688720703124, 'z': 9.222464794921875}
{'x': -0.47644613037109373, 'y': -0.41419688720703124, 'z': 9.208099584960937}
{'x': -0.5003881469726562, 'y': -0.469263525390625, 'z': 9.294290844726563}
{'x': -0.430956298828125, 'y': -0.373495458984375, 'z': 9.212887988281249}
{'x': -0.46208092041015625, 'y': -0.4285620971679687, 'z': 9.248801013183593}
{'x': -0.4525041137695312, 'y': -0.39743747558593745, 'z': 9.153032946777342}
{'x': -0.47884033203125, 'y': -0.43574470214843747, 'z': 9.169792358398437}
{'x': -0.32082302246093747, 'y': -0.4644751220703125, 'z': 9.334992272949219}
{'x': -0.43574470214843747, 'y': -0.603338818359375, 'z': 9.277531433105468}
{'x': -0.4213794921875, 'y': -0.40222587890625, 'z': 9.196128576660156}
{'x': -0.46686932373046874, 'y': -0.47884033203125, 'z': 9.239224206542968}
{'x': -0.44053310546874996, 'y': -0.6057330200195312, 'z': 9.220070593261719}
{'x': -0.5913678100585937, 'y': -0.5674257934570313, 'z': 9.220070593261719}
{'x': -0.5506663818359374, 'y': -0.38307226562499996, 'z': 9.062053283691405}
{'x': -0.4525041137695312, 'y': -0.45489831542968745, 'z': 9.167398156738281}
{'x': -0.46208092041015625, 'y': -0.4165910888671875, 'z': 9.165003955078124}
Traceback (most recent call last):
  File "/home/pi/test/imu.py", line 7, in <module>
    accelerometer_data = sensor.get_accel_data()
  File "/home/pi/.local/lib/python3.9/site-packages/mpu6050/mpu6050.py", line 153, in get_accel_data
    z = self.read_i2c_word(self.ACCEL_ZOUT0)
  File "/home/pi/.local/lib/python3.9/site-packages/mpu6050/mpu6050.py", line 84, in read_i2c_word
    low = self.bus.read_byte_data(self.address, register + 1)
OSError: [Errno 121] Remote I/O error
```

ugh... man this sucks

might be inevitable in the future to have a separate microcontroller controlling the hardware and attach it to the Pi

Anyway I can work with this, I tried this other code [here](https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi)

It does a little better, I had to do the [delay trick](https://stackoverflow.com/questions/52735862/getting-ioerror-errno-121-remote-i-o-error-with-smbus-on-python-raspberry-w) to improve it but eventually it still stops and fails.

I mean it would be nice to have a thread running that's constantly reading the MPU6050 but I can't keep it alive it seems... can restart it I suppose when it dies.

To the forums!

yeah it does better when nothing else is plugged in.

So the problem with the IMU not being able to run on its own continuously is I can't use it to estimate velocity/how far the robot actually moved.

I need to run that while it talks to the other half of the robot then compare the difference from stopped, moving, stopped to check if it moved as far as expected.

I'm having a bad... desperate idea... I'm thinking I will use a Seeeduino (small form factor) and use that to read the MPU6050 and then send it to the RPi which doesn't seem to make sense due to the i2c problem to begin with. But I could use serial to talk from Pi to Seeeduino.

10:12 AM

trying to have Seeeduino read IMU

Well I got it working... the issue is there is only one tx/rx port on the Pi it seems. So I would need to use SPI or if I2C cooperates, that.

I'm going to test the i2c reliability with the Pi to Seeeduino

BMS kicked in nice battery is at 3V though hmm

I got code running on the Seeeduino to read from MPU6050 but damn it'll suck if I have to do this route... have to do an i2c or SPI bridge between Pi/Seeeduino

I'm kind of blocked mentally until I figure out if this MPU problem is fixed or not...

Soon I'll start putting together the system design though.

11:38 AM

Sidetracked from charging

I'm going to work out the distance traveled by the wheels per command/come up with a command string sequence

5.17" absolute diameter (stubs)

5" pad diameter

circumference 2pir is 15.7"

it's more accurate than that but also this wheel is not a good circle, it has a lot of flat edges.

So each degree is 0.04"

Probably do mf_12 (degrees) ... ehhh

I'll use the inches and rotate degrees

12:09 PM

Kind of chilling, messing around

I'm working on the motion stuff

Trying to figure out if the wheels rotate in opposite directions at some degree, how many degrees did the robot turn?

Roughly 3.6" inner radius, using SketchUp to figure out the degrees turned

So 1" forward is 15.5 degrees

This is where self testing works well... the reality expectation vs. IMU in case of slippage and visual checking of known landmarks.

1:05 PM

Crap... I don't think I have this right, I did not factor in the speed of the rotation and time it runs for

It's not bad

1:24 PM

I just had a neat idea for the UI, I can import a glTf export of the sensor assembly and represent its state in 3D on a little window. Also show camera feed (possibly live) and decisions performed in steps below as a history will include drawing.

it moves 1 and 11/16" forward with 1 command

1.6875" at 250ms let me see if I do it longer does that matter, think it's just delay

Oh my god it goes farther, like twice as far hmm

at 150ms looks like it moves about 1.25"

Hmm dropped it to 1 degree apart and it doesn't move interesting

turning is good here

will need to spend more time on this to really understand what's happening

not just physically measure it, figure out some ratio and use it as a function
2:31 PM

ahhh.... so the IMU is still having problems.

If I unplug everything the connection is more stable but it still dies eventually

I'll try the other bus set one more time but yeah... I'll probably have to use SPI to connect to the Seeeduino that then connects to the IMU... ahhh man just more work

Damn... yeah it's gonna have to be done... I just have not used SPI before so I'll have to take time to figure out how to do that.

This looks like a nice [guide](https://roboticsbackend.com/raspberry-pi-master-arduino-uno-slave-spi-communication-with-wiringpi/)

I want to get to a good spot so I'm going to try this, it looks short.

I need to have bidirectional data messaging between them.

What will happen is the IMU will run on a fast loop that can dump data when requested by the Pi

Well this is cool the MOSI/MISO (soup)

I'm just gonna go for it...

3:39 PM

Not sure if I'm going to get this to work, I'm already burnt

Already having problems the SPI code won't compile hmm

Oh okay that code is for AVR not SAMD

https://forum.arduino.cc/t/error-expected-constructor-destructor-or-type-conversion-before/653777/2s

Ugh... I'm just gonna enable another serial set and use that

https://raspberrypi.stackexchange.com/questions/127265/multiple-uarts-on-the-40-pin

Ahh only thing that sucks is the serial buffer build up concern on the Seeeduino hmm

I will make this work even if it's ugly

ahh damn it's for pi4 not pi zero 2 w

hmm............. I could try software serial they said "error free" but idk

Alright this is not happening right now, I have to go with the SPI route because I've used software serial before and it was not good.

They're talking about error rates [here](https://forums.raspberrypi.com/viewtopic.php?t=35544).

ahh man... dang I'm spent now, need to do nothing for the rest of the day

### Saturday 08/06/2022

Ahh fresh day although it's already 5 PM now been working on it since 8 the wifi buggy

I forgot how this process works that I came up with for blob finding based on HSV

Referring to my [notes/old code](https://github.com/jdc-cunningham/slam-crappy/tree/master/vision)

- unable to localte libjasper-dev, libpng12-dev

Will proceed without

I think this is the sequence of steps:

- 1D
- 2D
- apply mask
- find contours

python3-opencv install seems to work... I forgot for SSH the matploglib gui won't show up so I was developing this on a Ubuntu VM back then.

10:23 PM

I'm just poking around... idk what happened to this IMU

It worked fine on its own, after it's in parallel with the ToF ranging it's not working anymore or very rarely.

I've seen some mentions it should use 3.3V...

So both the MPU6050 and VL53L0X can operate at 3.3V so I'll power it with that.

It's a little better but still broken

Yeah this is a problem, I have to figure out why it keeps doing this IO error

### Friday 08/05/2022

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

### Thursday 08/04/2022

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

11:54 PM
wow this thing is awesome... it's a unit... stands on its own

I can just program it wireless by SSH ha (not great, would actually git clone down)

<img src="./standing.JPG" width="500"/>

So tomorrow I'll build the tail dragger robot which is pretty straight forward.

Then I'll program the first navigation attempts... I still have an issue to deal with the MPU6050 i2c not being reliable... I tried another new MPU6050 and same issue... think it's related to the library or how I have two i2c devices... the tof one is rock solid though... that's interesting. Lidar is using serial so not affected.

### Wednesday 08/03/2022

Back on it. Feeling like I have left over energy.

I'm trying out hardware pwm as described [here](https://abyz.me.uk/rpi/pigpio/python.html#hardware_PWM)

5:35 PM
I have this strong urge/feeling of not wanting to do this... just so much work.

But the end result will be cool.

8:23 PM

Damn that's gonna take about 6 hrs to print oof

I'll interface with electronics in the meantime

### Monday 08/01/2022

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

### Saturday 07/30/2022

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