const dpadForward = document.getElementById('buggy-forward');
const dpadLeft = document.getElementById('buggy-left');
const dpadRight = document.getElementById('buggy-right');
const dpadBackward = document.getElementById('buggy-reverse');

const dpadBtns = [dpadForward, dpadLeft, dpadRight, dpadBackward];
const commLookup = {
  'forward': 'm_f',
  'left': 'm_l',
  'right': 'm_r',
  'backward': 'm_b',
  'stop': 'm_s'
};

const getMessage = (direction, unit) => {
  // ehh
  if (direction === 'buggy-forward') {
    return `_mfs_${unit}_mfe_`;
  } else if (direction === 'buggy-reverse') {
    return `_mbs_${unit}_mbe_`;
  } else if (direction === 'buggy-left') {
    return `_mls_${unit}_mle_`;
  } else if (direction === 'buggy-right') {
    return `_mrs_${unit}_mre_`;
  }
}

let activeDirection = '';

dpadBtns.forEach(dpadBtn => dpadBtn.addEventListener('click', (e) => {
  const whichDir = e.target.getAttribute('id');
  const forwardBackwardMotionUnit = document.getElementById('motion-distance');
  const turnMotionUnit = document.getElementById('rotate-angle');

  let msgToSend = "";

  if (whichDir === 'buggy-forward' || whichDir === 'buggy-backward') {
    msgToSend = getMessage(whichDir, forwardBackwardMotionUnit.value);
  } else {
    msgToSend = getMessage(whichDir, turnMotionUnit.value);
  }

  activeDirection = whichDir;
  socket.send(msgToSend);
  // appendMessage('ui', msgToSend);
}));
