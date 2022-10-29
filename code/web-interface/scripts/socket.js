let socketInterval = null;
let socket = null;
let wasConnected = false;

let displacement = 0;
let currentVelocity = 0; // in/s
let minY = 0;
let ySamples = 0;

const socketStatus = document.getElementById('socket-status');

const toInches = (m) => m * 39.3701;

// https://www.calculatorsoup.com/calculators/physics/displacement_v_a_t.php
const calculateDisplacement = (sampleAccel) => {
  const sampleTime = 0.1; // fixed 100ms
  const sampleVelocity = 0.1 * sampleAccel;
  // impure
  currentVelocity += sampleVelocity;
  displacement += (
    (sampleVelocity * sampleTime) + ((1/2) * sampleAccel * (sampleTime * sampleTime))
  );
};

const connectToNavigationDevice = () => {
  socket = new WebSocket('ws://192.168.1.156:5678'); // esp01 on robot

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
    socket.send('Hello robot!');
 
    // keep connection to esp01 alivew
    socketInterval = setInterval(() => {
      socket.send('poll');
    }, 1000);
  });
 
  // listen for messages from floating navigation sensor assembly
  socket.addEventListener('message', function (event) {
    const imuSample = JSON.parse(event.data);

    const yAccel = imuSample[0][1];

    ySamples += 1;

    console.log(ySamples, Date.now());

    if (yAccel < 0 && (yAccel * -1) < 0.01) return;
    if (yAccel > 0 && yAccel < 0.01) return;
    
    socketStatus.innerText = yAccel > 0 ? 'pos y' : 'neg y';

    // calculateDisplacement(toInches(yAccel));

    // console.log(`displacement: ${displacement} in`);
  });
 
  socket.addEventListener('close', function (event) {
    socketStatus.innerText = wasConnected ? 'connection lost, reconnecting...' : 'failed to connect, connecting...';
    clearInterval(socketInterval);
  });

  socket.addEventListener('error', function (event) {
    socketStatus.innerText = 'error connecting, trying again...';
    clearInterval(socketInterval);

    setTimeout(() => {
      connectToNavigationDevice();
    }, 1000);
  });
}

connectToNavigationDevice();