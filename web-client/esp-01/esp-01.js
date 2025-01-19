let esp01Connected = false;
let connectTimeout;
let espSocket;

const connectToEsp01 = () => {
  espSocket = new WebSocket('ws://192.168.1.159'); // esp01 on robot

  espSocket.addEventListener('open', (event) => {
    console.log(event);

    espSocket.send('yo');
  });

  espSocket.addEventListener('close', (event) => {
    espSocket = null;
    clearTimeout(connectTimeout);

    connectTimeout = setTimeout(() => {
      connectToEsp01();
    }, 1000);
  });
}

connectToEsp01();

const sendMsgToEsp01 = (msg) => {
  if (!espSocket) {
    return false;
  } else {
    espSocket.send(msg);

    return true;
  }
}
