// this file relies on statuses.js to exist before itself
let meshTelUploading = false;
let socketInterval = null;
let socket = null;
let msgAppendCounter = 0;

const socketStatus = document.getElementById('socket-status');
const messages = document.getElementById('messages');

const appendMessage = (from, msg) => {
  messages.innerText = `from: ${from}, msg ${msg} \n` + messages.innerText;
  msgAppendCounter += 1;

  if (msgAppendCounter === 10) {
    msgAppendCounter = 0;
    messages.innerText = '';
  }
}

const connectToRobot = () => {
  socket = new WebSocket('ws://192.168.1.195:80'); // esp01 on robot

  // connection opened, send messages to robot
  socket.addEventListener('open', function (event) {
    socketStatus.innerText = 'connected';
    socket.send('Hello robot!');
 
    // keep connection to esp01 alive
    socketInterval = setInterval(() => {
      socket.send('poll');
      appendMessage('ui', 'poll');
    }, 1000);
  });
 
// listen for messages from robot
  socket.addEventListener('message', function (event) {
    const robotMsg = event.data;
    appendMessage('robot', robotMsg);
  });
 
  socket.addEventListener('close', function (event) {
    socketStatus.innerText = 'connection lost';
    clearInterval(socketInterval);
    if (!meshTelUploading) connectToRobot();
 });
}

connectToRobot();