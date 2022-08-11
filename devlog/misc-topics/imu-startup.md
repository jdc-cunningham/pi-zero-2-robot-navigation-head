So this thing is problematic...

I have to wiggle wires, run `$sudo i2cdetect -y 1` a couple of times to see it pop up eg. `0x68` then I have to run the `mpu9250.py` script a few times before it starts dumping data.

So I'll have an external notification to get this thing going (web interface).

Then once it's going it should be good to be started as a thread and run/be ready to be sampled.
