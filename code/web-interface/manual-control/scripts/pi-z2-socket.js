let piSocketInterval = null;
let piSocket = null;

const piSocketStatus = document.getElementById('pi-socket-status');

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
  });
 
  piSocket.addEventListener('close', function (event) {
    piSocketStatus.innerText = 'pi connection lost';
    clearInterval(piSocketInterval);
 });
}

connectToPiZero2();