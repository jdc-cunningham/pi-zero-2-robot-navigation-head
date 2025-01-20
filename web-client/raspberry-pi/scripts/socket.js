let socketInterval = null;

const connectToRobot = () => {
  const socket = new WebSocket('ws://192.168.1.155:5678'); // raspberry pi

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
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