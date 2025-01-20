const statusText = document.querySelector(".app__right-buttons-line h2");
const statusIcon = document.querySelector(".app__right-buttons-line-connection-status");

const setConnected = (connected) => {
  if (connected) {
    statusIcon.classList += " connected";
    statusText.innerText = "Status: connected";
  } else {
    statusIcon.classList = "app__right-buttons-line-connection-status";
    statusText.innerText = "Status: disconnected";
  }
}
