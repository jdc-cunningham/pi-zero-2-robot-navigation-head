// this has to be hosted somewhere, in my case a Raspberry Pi Apache Web Server
// needs CORS
const baseGlbPath = "http://192.168.1.144/3d-files/";
const robotGlbFilename = "basic-robot-model.glb";
const loader = new THREE.GLTFLoader();
const gltfs = {};
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 2000);
const orangeMaterial = new THREE.LineBasicMaterial({color: 0xffa500});
const canvas = document.getElementById("threejs-canvas");
const renderer = new THREE.WebGLRenderer({ canvas: canvas }); // https://stackoverflow.com/a/21646450/2710227

const degToRad = (deg) => deg * 0.0174533;

const plotLine = (sensorX, sensorY, sensorZ) => {
  const points = [];

  points.push(new THREE.Vector3(0.87, 0.63, 6.93)); // wide sensor center
  points.push(new THREE.Vector3(sensorX, sensorY, sensorZ));

  const geometry = new THREE.BufferGeometry().setFromPoints( points );

  const tubeGeometry = new THREE.TubeGeometry(
    new THREE.CatmullRomCurve3(points),
    512,// path segments
    0.1,// THICKNESS
    8, //Roundness of Tube
    false //closed
  );

  const line = new THREE.Line(tubeGeometry, orangeMaterial);

  scene.add( line );
  renderer.render(scene, camera);
}

const getSensorX = (sweepAngle, sensorDistance, direction = "") => {
  const multipler = direction ? -1 : 1;
  const distanceRadians = degreesToRadians(Math.abs(parseFloat(sweepAngle)));
  return parseFloat((sensorDistance * Math.cos(distanceRadians)).toFixed(2)) * multipler;
}

const getSensorY = (tiltAngle, sensorDistance) => {
  const floorAngle = tiltAngle;
  const distanceRadians = degreesToRadians(Math.abs(parseFloat(floorAngle)));
  return parseFloat(((sensorDistance * Math.sin(distanceRadians))).toFixed(2));
}

const getSensorZ = (tiltAngle, distance) => {
  const distanceRadians = degreesToRadians(Math.abs(parseFloat(tiltAngle)));
  return parseFloat((distance * Math.sin(distanceRadians)).toFixed(2));
}

// const inchToMeter = inches => inches * 39.3701; // way too big
const inchToMeter = inches => inches * 1;

// gltf uses meters
const sampleFloorSensorScanCoordinateDataPair = {
  "54-15-r": inchToMeter(8.93),
  "54-35-r": inchToMeter(8.78),
  "54-60-r": inchToMeter(8.42),
  "54-20-l": inchToMeter(9.09),
  "54-40-l": inchToMeter(9.05),
  "54-60-l": inchToMeter(8.97),
  "54-85-l": inchToMeter(8.74),
  "35-15-r": inchToMeter(11.89),
  "35-30-r": inchToMeter(11.31),
  "35-45-r": inchToMeter(11.0),
  "35-60-r": inchToMeter(10.72),
  "35-15-l": inchToMeter(12.56),
  "35-30-l": inchToMeter(12.32),
  "35-45-l": inchToMeter(11.89),
  "35-60-l": inchToMeter(11.54),
  "35-75-l": inchToMeter(11.31),
  "15-20-r": inchToMeter(25.74),
  "15-40-r": inchToMeter(22.74),
  "15-60-r": inchToMeter(21.06),
  "15-20-l": inchToMeter(26.56),
  "15-40-l": inchToMeter(25.27),
  "15-60-l": inchToMeter(22)
};

const sampleFloorSensorScanAngles = [
  [54, [15, 35, 60], [20, 40, 60, 85]],
  [35, [15, 30, 45, 60], [15, 30, 45, 60, 75]],
  [15, [20, 40, 60], [20, 40, 60]]
];

const sampleFloorSensorScanDistanecs = [
  [[8.93, 8.78, 8.42], [9.09, 9.05, 8.97, 8.74]],
  [[11.89, 11.31, 11.0, 10.72], [12.56, 12.32, 11.89, 11.54, 11.31]],
  [[25.74, 22.74, 21.06], [26.56, 25.27, 22.0]]
];

const plotSensorBeams = () => {
  sampleFloorSensorScanAngles.forEach(tiltSampleSet => {
    sampleFloorSensorScanAngles.forEach(tiltSampleData => {
      tiltAngle = tiltSampleData[0];

      // right
      tiltSampleData[1].forEach(sweepAngle => {
        const sensorX = getSensorX(sweepAngle, sampleFloorSensorScanCoordinateDataPair[`${tiltAngle}-${sweepAngle}-r`]);
        const sensorY = getSensorY(tiltAngle, sampleFloorSensorScanCoordinateDataPair[`${tiltAngle}-${sweepAngle}-r`]) - 6.93;
        const sensorZ = getSensorZ(tiltAngle, sampleFloorSensorScanCoordinateDataPair[`${tiltAngle}-${sweepAngle}-r`]);

        plotLine(sensorX, sensorZ, sensorY); // due to swapping y-z
      });

      // left
      tiltSampleData[2].forEach(sweepAngle => {
        const sensorX = getSensorX(sweepAngle, sampleFloorSensorScanCoordinateDataPair[`${tiltAngle}-${sweepAngle}-l`], "left");
        const sensorY = getSensorY(tiltAngle, sampleFloorSensorScanCoordinateDataPair[`${tiltAngle}-${sweepAngle}-l`], "left") - 6.93;
        const sensorZ = getSensorZ(tiltAngle, sampleFloorSensorScanCoordinateDataPair[`${tiltAngle}-${sweepAngle}-l`], "left");

        plotLine(sensorX, sensorZ, sensorY);
      });
    });    
  });
}

const threejsPlotChart = () => {
  // https://threejs.org/docs/#manual/en/introduction/Creating-a-scene
  THREE.Object3D.DefaultUp.set(0, 0, 1); // set Z as vertical axes
  // 10 z distanece
  const canvasParent = document.querySelector('.app__left-plot');

  scene.background = new THREE.Color( 0xffffff );

  renderer.setSize(canvasParent.offsetWidth, canvasParent.offsetWidth); // add false for lower resolution after dividing x/y values
  // renderer.setPixelRatio(window.devicePixelRatio);
  // renderer.setPixelRatio(2); // looks great
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
  const divisions = 100;
  const gridHelper = new THREE.GridHelper(size, divisions);
  const zVector = new THREE.Vector3(0, 0, 1);
  const yVector = new THREE.Vector3(0, 1, 0);
  gridHelper.rotateX(Math.PI / 2); // https://stackoverflow.com/a/58554774/2710227
  gridHelper.lookAt(yVector);
  scene.add(gridHelper);

  controls.update();

  function animate() {
    requestAnimationFrame( animate );
    // required if controls.enableDamping or controls.autoRotate are set to true
    controls.update();
    renderer.render( scene, camera );
  }

  // camera
  camera.position.set( 0, 0, 1 );
  camera.position.z = 30; // zoom out
  // camera.lookAt( 0, 0, 0 );

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

  // referencing my Twerk Lidar Robot project
  // https://github.com/jdc-cunningham/twerk-lidar-robot/blob/dev/web-simulator/index.html
  const loadFile = (filePath) => {
    loader.load(
      // resource URL
      `${baseGlbPath}/${filePath}`,
      // called when the resource is loaded
      function ( gltf ) {

        gltfs[filePath.replace('.glb', '')] = {
          handle: gltf,
        };

        scene.add(new THREE.AmbientLight(0xdddddd)); // controls brightness of colors
        // gltf.scene.position.x=10
        scene.add( gltf.scene );

        gltf.animations; // Array<THREE.AnimationClip>
        gltf.scene; // THREE.Group
        gltf.scene.scale.set(39.3701, 39.3701, 39.3701); // inch to meter
        gltf.scenes; // Array<THREE.Group>
        gltf.cameras; // Array<THREE.Camera>
        gltf.asset; // Object

        renderer.render( scene, camera );
        gltfs["basic-robot-model"].handle.scene.rotateX(degToRad(90)); // match blue as Z axis
        gltfs["basic-robot-model"].handle.scene.rotateY(degToRad(-90)); // match blue as Z axis
        plotSensorBeams();
      },
      // called while loading is progressing
      function ( xhr ) {
        console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
      },
      // called when loading has errors
      function ( error ) {
        console.log( 'An error happened' );
      }
    );
  }

  loadFile(robotGlbFilename);
  animate();
};

threejsPlotChart();
