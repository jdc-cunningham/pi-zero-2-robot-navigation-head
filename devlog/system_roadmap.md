- [ ] general
  - [ ] add braking
    - this thing is top heavy, hence it carries around this heavy 5/8" chisel tool for a counter mass
      the abrupt stopping makes the robot nearly tip over and generally nasty vibrations
      currently accounted for in the pan servo case with long photo delays eg. 3 seconds per shot, up to 45 seconds of extra delay
- [ ] vision stack
  - [ ] panorama
    - [ ] determine mostly uniform or lots of small bits (more images to gen pan)
    - [ ] determine light or dark (dark pan not possible)
    - [x] generate panorama
      - used OpenCV's stitcher
  - [x] find blobs
    - [x] crude approach with random HSV sampling and contours
  - [ ] ranging
    - [ ] accurately point the beams at things and get their distances
          account for geometry offset issues
- [ ] accurately measure displacement'
  - [ ] factor in offset due to switching out MPU6050 with MPU9250
  - [x] measure rotation
    - did this with TLR project
  - [ ] measure pitch
    - have not been able to accurately do this
- [ ] navigation
  - [ ] map surroundings and be able to accept a waypoint, should not need to rescan
        if sufficient data available
- [ ] motion
  - [ ] fix the possibilty of serial buffer overflow, robot loses control
        due to dumb websocket

