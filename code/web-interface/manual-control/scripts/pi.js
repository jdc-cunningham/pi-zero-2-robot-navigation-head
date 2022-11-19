const cameraUp = document.getElementById('camera-up');
const cameraLeft = document.getElementById('camera-left');
const cameraCenter = document.getElementById('camera-center');
const cameraRight = document.getElementById('camera-right');
const cameraDown = document.getElementById('camera-down');
const probeTof = document.getElementById('probe-tof');
const probeLidar = document.getElementById('probe-lidar');

const buttons = [
  cameraUp,
  cameraLeft,
  cameraCenter,
  cameraRight,
  cameraDown,
  probeTof,
  probeLidar,
];

buttons.forEach(button => {
  button.addEventListener('click', (e) => {
    const id = e.target.id;

    if (id === "camera-left") piSocket.send('left');
    if (id === "camera-right") piSocket.send('right');
    if (id === "camera-up") piSocket.send('up');
    if (id === "camera-down") piSocket.send('down');
    if (id === "camera-center") piSocket.send('center');
    if (id === "probe-tof") piSocket.send('tof');
    if (id === "probe-lidar") piSocket.send('lidar');
  });
});