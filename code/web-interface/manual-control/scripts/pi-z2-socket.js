let piSocketInterval = null;
let piSocket = null;
let activeSensor;

const piSocketStatus = document.getElementById('pi-socket-status');
const tofVal = document.getElementById('tof-value');
const lidarVal = document.getElementById('lidar-value');

const maxDigit = (str) => {
  const strParts = str.split('.');
  return strParts[0] + "." + strParts[1].substring(0, 2);
}

const connectToPiZero2 = () => {
  piSocket = new WebSocket('ws://192.168.1.156:5678'); // esp01 on robot

  // connection opened, send messages to robot
  piSocket.addEventListener('open', function (event) {
    piSocketStatus.innerText = 'pi connected';
    piSocket.send('Hello robot!');
 
    // keep connection to esp01 alive
    piSocketInterval = setInterval(() => {
      piSocket.send('poll');
    }, 1000);
  });
 
// listen for messages from robot
  piSocket.addEventListener('message', function (event) {
    const robotMsg = event.data;

    if (activeSensor && robotMsg.indexOf('.') !== -1) {
      if (activeSensor === 'tof') {
        tofVal.innerText = `${maxDigit(robotMsg)} in`;
      } else {
        lidarVal.innerText = `${maxDigit(robotMsg)} in`;
      }
    }
  });
 
  piSocket.addEventListener('close', function (event) {
    piSocketStatus.innerText = 'pi connection lost';
    clearInterval(piSocketInterval);
    connectToPiZero2();
 });
}

connectToPiZero2();