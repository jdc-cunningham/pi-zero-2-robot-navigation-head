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

const plotLine = (sensor, sensorDistance) => {
  const points = [];

  points.push(new THREE.Vector3(sensor.x, sensor.y, sensor.z)); // wide sensor center
  points.push(new THREE.Vector3(sensorDistance.x, sensorDistance.y, sensorDistance.z));

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

const getDistanceX = (sweepAngle, sensorDistance, direction = "") => {
  const multipler = 1;
  const distanceRadians = degreesToRadians(Math.abs(parseFloat(sweepAngle)));
  return parseFloat((sensorDistance * Math.sin(distanceRadians)).toFixed(2)) * multipler;
}

const getDistanceY = (sweepAngle, sensorDistance) => {
  const distanceRadians = degreesToRadians(Math.abs(parseFloat(sweepAngle)));
  return parseFloat(((sensorDistance * Math.cos(distanceRadians))).toFixed(2));
}

const getDistanceZ = (tiltAngle, sensorDistance) => {
  const distanceRadians = degreesToRadians(Math.abs(parseFloat(tiltAngle)));
  return parseFloat((sensorDistance * Math.sin(distanceRadians)).toFixed(2));
}

// const inchesToMeter = inches => inches * 39.3701; // way too big
// only needed for GLTF import
const inchesToMeter = inches => inches * 1;

// y is z (SketchUp to ThreeJS)
// [x, z, y]
// tfmini-s is on same x-axis but offset by 1.8 (0.9 mirrored)
// +0.14 z (forward)
const sampleFloorScanSensorCoordinate = {
  "54-0-r": [0.86, 6.28, 0.28],
  "54-15-r": [0.89, 6.28, 0],
  "54-35-r": [0.84, 6.28, -0.31],
  "54-60-r": [0.63, 6.28, -0.64],
  "54-20-l": [0.73, 6.28, 0.51],
  "54-40-l": [0.52, 6.28, 0.73],
  "54-60-l": [0.24, 6.28, 0.86],
  "54-85-l": [-0.15, 6.28, 0.88],

  "35-0-r": [0.86, 6.47, 0.42],
  "35-15-r": [0.94, 6.47, 0.18],
  "35-30-r": [0.96, 6.47, -0.07],
  "35-45-r": [0.91, 6.47, -0.31],
  "35-60-r": [0.8, 6.47, -0.54],
  "35-15-l": [0.73, 6.47, 0.63],
  "35-30-l": [0.54, 6.47, 0.8],
  "35-45-l": [0.31, 6.47, 0.91],
  "35-60-l": [0.07, 6.47, 0.96],
  "35-75-l": [-0.18, 6.47, 0.94],

  "15-0-r": [0.86, 6.73, 0.55],
  "15-20-r": [1, 6.73, 0.22],
  "15-40-r": [1.02, 6.73, -0.13],
  "15-60-r": [0.91, 6.73, -0.47],
  "15-20-l": [0.62, 6.73, 0.81],
  "15-40-l": [0.31, 6.73, 0.98],
  "15-60-l": [-0.04, 6.73, 1.02]
};

// gltf uses meters
const sampleFloorScanSensorDistance = {
  "54-0-r": 9.2,
  "54-15-r": 8.93,
  "54-35-r": 9.01,
  "54-60-r": 8.58,
  "54-20-l": 9.48,
  "54-40-l": 9.13,
  "54-60-l": 8.97,
  "54-85-l": 8.74,

  "35-0-r": 12.13,
  "35-15-r": 11.97,
  "35-30-r": 11.54,
  "35-45-r": 11.15,
  "35-60-r": 11.84,
  "35-15-l": 10.93,
  "35-30-l": 11.36,
  "35-45-l": 12.89,
  "35-60-l": 11.74,
  "35-75-l": 11.12,

  "15-0-r": 26.29,
  "15-20-r": 25.27,
  "15-40-r": 23.63,
  "15-60-r": 22.15,
  "15-20-l": 27.11,
  "15-40-l": 27.11, // 319.41 outlier example, pretty much nothing measured/infinite, cap to largest value in set
  "15-60-l": 26.75
};

const sampleFloorSensorScanAngles = [
  [54, [0, 15, 35, 60], [20, 40, 60, 85]],
  [35, [0, 15, 30, 45, 60], [15, 30, 45, 60, 75]],
  [15, [0, 20, 40, 60], [20, 40, 60]]
];

const sampleFloorSensorScanDistanecs = [
  // [[9, 8.93, 8.78, 8.42], [9.09, 9.05, 8.97, 8.74]],
  // [[12, 11.89, 11.31, 11.0, 10.72], [12.56, 12.32, 11.89, 11.54, 11.31]],
  // [[26, 25.74, 22.74, 21.06], [26.56, 25.27, 22.0]]
  [[9.2, 8.93, 9.01, 8.58], [9.48, 9.13, 8.97, 8.74]],
  [[12.13, 11.97, 11.54, 11.15, 10.84], [11.93, 12.36, 11.89, 11.74, 11.12]],
  [[26.29, 25.27, 23.63, 22.15], [27.11, 319.41, 26.75]]
];

const plotSensorBeams = () => {
  sampleFloorSensorScanAngles.forEach(tiltSampleData => {
    tiltAngle = tiltSampleData[0];

    // right
    tiltSampleData[1].forEach(sweepAngle => {
      const distanceX = getDistanceX(sweepAngle, sampleFloorScanSensorDistance[`${tiltAngle}-${sweepAngle}-r`]);
      const distanceY = getDistanceY(sweepAngle, sampleFloorScanSensorDistance[`${tiltAngle}-${sweepAngle}-r`]);
      const distanceZ = getDistanceZ(tiltAngle, sampleFloorScanSensorDistance[`${tiltAngle}-${sweepAngle}-r`]);
      const sensorCoordinate = sampleFloorScanSensorCoordinate[`${tiltAngle}-${sweepAngle}-r`];

      plotLine(
        {
          x: -1 * sensorCoordinate[0],
          y: sensorCoordinate[1],
          z: sensorCoordinate[2]
        },
        {
          x: -1 * distanceX,
          y: distanceZ - sensorCoordinate[1], // sensor is above horizon
          z: distanceY
        }
      );
    });

    // left
    tiltSampleData[2].forEach(sweepAngle => {
      const distanceX = getDistanceX(sweepAngle, sampleFloorScanSensorDistance[`${tiltAngle}-${sweepAngle}-l`], "left");
      const distanceY = getDistanceY(sweepAngle, sampleFloorScanSensorDistance[`${tiltAngle}-${sweepAngle}-l`], "left");
      const distanceZ = getDistanceZ(tiltAngle, sampleFloorScanSensorDistance[`${tiltAngle}-${sweepAngle}-l`], "left");
      const sensorCoordinate = sampleFloorScanSensorCoordinate[`${tiltAngle}-${sweepAngle}-l`];

      plotLine(
        {
          x: sensorCoordinate[0],
          y: sensorCoordinate[1],
          z: sensorCoordinate[2]
        },
        {
          x: distanceX,
          y: distanceZ - sensorCoordinate[1], // sensor is above horizon
          z: distanceY
        }
      );
    });
  });
}

const threejsPlotChart = () => {
  // https://threejs.org/docs/#manual/en/introduction/Creating-a-scene
  // THREE.Object3D.DefaultUp.set(0, 0, 1); // set Z as vertical axes
  // 10 z distanece
  const canvasParent = document.querySelector('.app__left-plot');

  scene.background = new THREE.Color( 0xffffff );

  renderer.setSize(canvasParent.offsetWidth, canvasParent.offsetHeight); // add false for lower resolution after dividing x/y values
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
  // gridHelper.rotateX(Math.PI / 2); // https://stackoverflow.com/a/58554774/2710227
  // gridHelper.lookAt(yVector);
  scene.add(gridHelper);

  controls.update();

  function animate() {
    requestAnimationFrame( animate );
    // required if controls.enableDamping or controls.autoRotate are set to true
    controls.update();
    renderer.render( scene, camera );
  }

  // camera
  // camera.position.set( 0, 1, 0 );
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
        // gltfs["basic-robot-model"].handle.scene.rotateX(degToRad(90)); // match blue as Z axis
        // gltfs["basic-robot-model"].handle.scene.rotateY(degToRad(-90)); // match blue as Z axis
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
