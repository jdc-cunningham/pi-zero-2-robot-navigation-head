const cmdInp = document.querySelector(".app__right-commands-input");
const sendCmdBtn = document.querySelector(".app__right-commands-btn");

sendCmdBtn.addEventListener('click', () => {
  if (robotConnected) {
    msgRobot(cmdInp.value);
  }
});