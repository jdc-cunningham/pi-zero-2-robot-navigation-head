let socketInterval = null;
let socket = null;
let wasConnected = false;

const socketStatus = document.getElementById('socket-status');

const connectToNavigationDevice = () => {
  socket = new WebSocket('ws://192.168.1.228:5678'); // esp01 on robot

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
    socket.send('Hello robot!');
 
    // keep connection to esp01 alive
    socketInterval = setInterval(() => {
      socket.send('poll');
    }, 1000);
  });
 
  // listen for messages from floating navigation sensor assembly
  socket.addEventListener('message', function (event) {
    const msg = event.data;
    console.log(msg);
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