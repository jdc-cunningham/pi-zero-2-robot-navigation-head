const threejsPlotChart = () => {
  // https://threejs.org/docs/#manual/en/introduction/Creating-a-scene
  THREE.Object3D.DefaultUp.set(0, 0, 1); // set Z as vertical axes
  const scene = new THREE.Scene();
  // 10 z distanece
  const camera = new THREE.PerspectiveCamera(100, window.innerWidth / window.innerHeight, 0.1, 1000);
  const canvas = document.getElementById("threejs-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas: canvas }); // https://stackoverflow.com/a/21646450/2710227
  const canvasParent = document.querySelector('.app__body-right');

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

  const meshPoints = {};
  const floorToSensorOffset = 3.125;
  const processOrder = ['tilt-up-2', 'tilt-up-1', 'level', 'tilt-down-1', 'tilt-down-2'];
  const tiltMap = {
    'tilt-up-2': 18.5,
    'tilt-up-1': 11.4,
    'level': 1.6,
    'tilt-down-1': -8.8,
    'tilt-down-2': -16.8
  };

  // offsets
  const getAdjustedTofValue = (sampleKey, originalTofValue) => {
    return originalTofValue;

    if (sampleKey === "level") {
      return originalTofValue;
    } else if (sampleKey === 'tilt-up-2') {
      return originalTofValue - 1.05;
    } else if (sampleKey === 'tilt-up-1') {
      return originalTofValue - 0.69;
    } else if (sampleKey === 'tilt-down-1') {
      return originalTofValue - 0.18;
    } else {
      return originalTofValue - 0.9;
    }
  }

  const getAdjustedAngle = (measurements, end, currentIndex, beyondMidpoint, sampleKey) => {
    // counter clockwise direction eg. right to left
    if (sampleKey === 'tilt-up-2' || sampleKey === 'level' || sampleKey === 'tilt-down-1') {
      if (end < 0 && !beyondMidpoint) {
        const flippedArray = measurements.reverse();
        return parseFloat(flippedArray[currentIndex]) * -1;
      } else {
        return parseFloat(measurements[currentIndex]);
      }
    } else {
      if (!beyondMidpoint) {
        return measurements.reverse()[currentIndex] * -1;
      } else {
        return measurements[currentIndex];
      }
    }
  }

  processOrder.forEach(sampleKey => {
    const preppedTofData = sensorSamples[sampleKey]['tof-samples'].split('\n').map(s => s.trim());
    const preppedSweepAngleData = sensorSamples[sampleKey]['sweep-angles'].split('\n').map(s => s.trim());

    let trimmedTofData = [];
    let trimmedSweepAngleData = [];

    // 80/120 original
    // 60/90

    if (sensorSamples[sampleKey]?.trim) {
      if (sensorSamples[sampleKey].trim === 'end') {
        trimmedTofData = preppedTofData.slice(0, 60);
        trimmedSweepAngleData = preppedSweepAngleData.slice(0, 60);
      } else {
        trimmedTofData = preppedTofData.slice(30, preppedTofData.length);
        trimmedSweepAngleData = preppedSweepAngleData.slice(30, preppedTofData.length);
      }
    } else {
      trimmedTofData = preppedTofData;
      trimmedSweepAngleData = preppedSweepAngleData;
    }

    meshPoints[sampleKey] = (
      trimmedTofData.map((distance, index) => {
        const adjustedAngle = getAdjustedAngle(
          (index < 30)
            ? trimmedSweepAngleData.slice(0, 30)
            : trimmedSweepAngleData.slice(30, trimmedSweepAngleData.length),
          trimmedSweepAngleData[29],
          (index < 30) ? index : (index - 30),
          index > 29 ? true : false
        );

        const adjustedDistance = getAdjustedTofValue(sampleKey, distance);

        return [
          parseFloat(getXCoordinate(adjustedAngle, adjustedDistance).toFixed(2)),
          parseFloat(getYCoordinate(adjustedAngle, adjustedDistance, sampleKey).toFixed(2)),
          parseFloat(getZCoordinate(tiltMap[sampleKey], adjustedDistance, floorToSensorOffset).toFixed(2))
        ];
      })
    );
  });

  const rangeFilterOff = true;

  Object.keys(meshPoints).forEach((sampleKey, sampleKeyIndex) => {
    if (sampleKey !== 'tilt-down-2') {
      const points = []; // for line
      const samplePlane = meshPoints[sampleKey];
      console.log(samplePlane);

      let nextPoints;
          
      if (sampleKey === 'tilt-up-2' || sampleKey === 'tilt-down-1') {
        nextPoints = meshPoints[processOrder[sampleKeyIndex + 1]].reverse();
      } else {
        nextPoints = meshPoints[processOrder[sampleKeyIndex + 1]];
      }

      samplePlane.forEach((coordinate, coordinateIndex) => {
        if (coordinateIndex < samplePlane.length - 1) {
          const planePoints = [
            coordinate,
            samplePlane[coordinateIndex + 1],
            nextPoints[coordinateIndex],
            nextPoints[coordinateIndex + 1]
          ];

          plotFourPointsAsPlane(planePoints);
        }

        points.push(new THREE.Vector3(coordinate[0], coordinate[1], coordinate[2]));
      });
      
      const geometry = new THREE.BufferGeometry().setFromPoints( points );
      const line = new THREE.Line( geometry, lineMaterial );
      scene.add( line );
    }
  });

  renderer.render(scene, camera);
  animate();
};