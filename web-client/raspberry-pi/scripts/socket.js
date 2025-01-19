// this file relies on statuses.js to exist before itself
let meshTelUploading = false;
let socketInterval = null;

const connectToRobot = () => {
  const socket = new WebSocket('ws://192.168.1.155:5678'); // esp01 on robot

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
    socket.send('Hello robot!');
    sentMsg('Hello robot!');
    setRobotConnected(true);
 
    // keep connection to esp01 alive
    socketInterval = setInterval(() => {
      socket.send('poll');
      sentMsg('poll');
    }, 1000);
  });
 
// listen for messages from robot
  socket.addEventListener('message', function (event) {
    const robotMsg = event.data;

    receivedMsg(robotMsg);

    if (meshTelUploading) {
      meshTelData += robotMsg;
    }

    if (!meshTelData && robotMsg.indexOf('mtel_start') !== -1) {
      meshTelUploading = true;
      meshTelData += robotMsg;

      // fallback unset
      setTimeout(() => {
        if (meshTelUploading) meshTelUploading = false;
      }, 120000); // 2 mins seems like a long time but it does take close to that, over 1 minute anyway
    }

    if (robotMsg.indexOf('mtel_end') !== -1) {
      meshTelUploading = false;
      meshPlot(meshTelData);
    }
  
    batteryVoltage(robotMsg);
    upsideDown(robotMsg);
  });
 
  socket.addEventListener('close', function (event) {
    clearInterval(socketInterval);
    if (!meshTelUploading) connectToRobot();
 });
}

connectToRobot();