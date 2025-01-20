const threejsPlotChart = () => {
  // https://threejs.org/docs/#manual/en/introduction/Creating-a-scene
  THREE.Object3D.DefaultUp.set(0, 0, 1); // set Z as vertical axes
  const scene = new THREE.Scene();
  // 10 z distanece
  const camera = new THREE.PerspectiveCamera(100, window.innerWidth / window.innerHeight, 0.1, 1000);
  const canvas = document.getElementById("threejs-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas: canvas }); // https://stackoverflow.com/a/21646450/2710227
  const canvasParent = document.querySelector('.app__left-plot');

  scene.background = new THREE.Color( 0xffffff );

  renderer.setSize(canvasParent.offsetWidth, canvasParent.offsetWidth); // add false for lower resolution after dividing x/y values
  // renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setPixelRatio(2); // looks great
  // https://discourse.threejs.org/t/render-looks-blurry-and-pixelated-even-with-antialias-true-why/12381/5

  // add orbit controls
  const controls = new THREE.OrbitControls( camera, renderer.domElement );
  const axesHelper = new THREE.AxesHelper(70);
  // const controls = new OrbitControls( camera, renderer.domElement );

  // add axes helper
  // x = red, y = green, z = blue
  // east, north, down
  scene.add(axesHelper);

  // add grid overlay
  const size = 100;
  const divisions = 10;
  const gridHelper = new THREE.GridHelper(size, divisions);
  // const zVector = new THREE.Vector3(0, 0, 1);
  gridHelper.rotateX(Math.PI / 2); // https://stackoverflow.com/a/58554774/2710227
  // gridHelper.lookAt(zVector);
  scene.add(gridHelper);

  controls.update();

  function animate() {
    requestAnimationFrame( animate );
    // required if controls.enableDamping or controls.autoRotate are set to true
    controls.update();
    renderer.render( scene, camera );
  }

  // camera
  camera.position.set( 0, 0, 100 );
  camera.lookAt( 0, 0, 0 );

  // line material
  let material = new THREE.LineBasicMaterial({ color: 0x00FF00 });
  let lineMaterial = new THREE.LineBasicMaterial({ color: 0x0000FF }); // FF0000 red

  const blue = 0x0000FF;
  const red = 0xFF0000;
  const green = 0x00FF00;

  // to make distinguishable panels, will eventually add a nice color pallete/ranging
  const getRandomHex = (returnRandom = true) => {
    if (!returnRandom) {
      return '#B6B6B6';
    }
    // https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
    var result           = '';
    var characters       = 'abcdef0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < 6; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return parseInt(`0x${result}`, 16);
  }

  // plot mesh
  const plotFourPointsAsPlane = (planePoints) => {
    let points = [];

    planePoints.forEach((panelPoint) => {
      points.push(new THREE.Vector3(panelPoint[0], panelPoint[1], panelPoint[2]));
    });

    material = new THREE.LineBasicMaterial({ color: getRandomHex() });
    meshGeometry = new THREE.ConvexGeometry( points ); // points = vertices array
    mesh = new THREE.Mesh(meshGeometry, material);
    scene.add(mesh);
  }

  renderer.render(scene, camera);
  animate();
};

threejsPlotChart();
