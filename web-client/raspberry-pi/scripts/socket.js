let socketInterval = null;
const telemetryDisplay = document.querySelector('.app__left-telemetry');

const updateTelemetryDisplay = (from, msg) => {
  telemetryDisplay.innerText = `${from}:${msg}` + '\n' + telemetryDisplay.innerText;
}

const connectToRobot = () => {
  updateTelemetryDisplay('client', 'connecting to robot...');
  
  const socket = new WebSocket('ws://192.168.1.155:5678'); // raspberry pi

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
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
    setConnected(false);
    clearInterval(socketInterval);
    connectToRobot();
 });
}

connectToRobot();
