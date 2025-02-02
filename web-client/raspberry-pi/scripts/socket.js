let socketInterval = null;
let robotConnected = false;
let socket;

const telemetryDisplay = document.querySelector('.app__left-telemetry');

const updateTelemetryDisplay = (from, msg) => {
  telemetryDisplay.innerText = `${from}: ${msg}` + '\n' + telemetryDisplay.innerText;
}

const msgRobot = (msg) => {
  if (robotConnected) {
    updateTelemetryDisplay("client", "send: " + msg);
    socket.send(msg);
  }
}

const receivedMsg = (msg) => {
  if (robotConnected) {
    updateTelemetryDisplay("robot", "recevied: " + msg);
  }
}

const connectToRobot = () => {
  updateTelemetryDisplay('client', 'connecting to robot...');
  
  socket = new WebSocket('ws://192.168.1.155:5678'); // raspberry pi

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
    robotConnected = true;
    updateTelemetryDisplay('client', 'connected');
    setConnected(true);
    socket.send('Hello robot!');
  });
 
// listen for messages from robot
  socket.addEventListener('message', function (event) {
    const robotMsg = event.data;

    receivedMsg(robotMsg);
  });
 
  socket.addEventListener('close', function (event) {
    robotConnected = false;
    setConnected(false);
    clearInterval(socketInterval);
    connectToRobot();
 });
}

connectToRobot();
