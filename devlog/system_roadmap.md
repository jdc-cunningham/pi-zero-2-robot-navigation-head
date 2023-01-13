- [ ] **general**
  - [ ] add braking
    - this thing is top heavy, hence it carries around this heavy 5/8" chisel tool for a counter mass
      the abrupt stopping makes the robot nearly tip over and generally nasty vibrations
      currently accounted for in the pan servo case with long photo delays eg. 3 seconds per shot, up to 45 seconds of extra delay
- [ ] **vision stack**
  - [ ] panorama
    - [ ] add early fail check to stop other subsequent processes
      - ex. too dark, don't do panorama (onboard LED sucks)
      - ex. image is mostly uniform, use less photos (inner, farthest)
      - ex. no center marker for top image (this would be bad)
    - [ ] determine mostly uniform or lots of small bits (more images to gen pan)
    - [ ] determine light or dark (dark pan not possible)
    - [x] add copies to not have red + and x in actual pan used for blob finding
    - [ ] find red +/x center on pan crop output image
    - [x] generate panorama
      - used OpenCV's stitcher
  - [x] find blobs
    - [x] crude approach with random HSV sampling and contours
  - [ ] ranging
    - [ ] accurately point the beams at things and get their distances
          account for geometry offset issues
- [x] **pan/tilt command**
  - [x] figure out some formulas to get deg in and pwm ms out
  - [x] verify externally by camera that it's correct
    it's mostly correct
- [ ] **accurately measure displacement (IMU)**
  - [ ] factor in offset due to switching out MPU6050 with MPU9250
  - [x] measure rotation
    - did this with TLR project
  - [ ] measure pitch
    - have not been able to accurately do this
- [ ] **navigation**
  - [ ] map surroundings and be able to accept a waypoint, should not need to rescan
        if sufficient data available
- [ ] **motion**
  - [ ] fix the possibilty of serial buffer overflow, robot loses control
        due to dumb websocket

