const init2DMap = () => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 2000);
  const canvas = document.getElementById("map-2d-canvas");
  const robotCanvas = document.getElementById("robot-3d-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas: canvas });

  const mapToggleBtn = document.getElementById('map-toggle');

  mapToggleBtn.addEventListener('click', () => {
    robotCanvas.classList = "hidden";
    canvas.classList = "";
  });

  const canvasParent = document.querySelector('.app__left-plot');
  scene.background = new THREE.Color( 0xffffff );

  renderer.setSize(canvasParent.offsetWidth, canvasParent.offsetHeight);

  const controls = new THREE.OrbitControls( camera, renderer.domElement );
  const axesHelper = new THREE.AxesHelper(70);

  controls.enableRotate = false; // disable rotation
  scene.add(axesHelper);

  const size = 100;
  const divisions = 100;
  const gridHelper = new THREE.GridHelper(size, divisions);
  const zVector = new THREE.Vector3(0, 0, 1);
  const yVector = new THREE.Vector3(0, 1, 0);

  
  gridHelper.lookAt(yVector);
  scene.add(gridHelper);
  controls.update();

  function animate() {
    requestAnimationFrame( animate );
    // required if controls.enableDamping or controls.autoRotate are set to true
    controls.update();
    renderer.render( scene, camera );
  }

  camera.position.z = 30;

  scene.add(new THREE.AmbientLight(0xdddddd));

  renderer.render(scene, camera);

  animate();
}

init2DMap();
