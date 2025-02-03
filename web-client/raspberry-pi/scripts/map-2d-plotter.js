let mapScene;

const init2DMap = () => {
  const scene = new THREE.Scene();

  mapScene = scene;

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

  const size = 1000;
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

  camera.position.z = 100;

  scene.add(new THREE.AmbientLight(0xdddddd));

  renderer.render(scene, camera);

  animate();
}

init2DMap();

const plotFourPointsAsPlane = (planePoints) => {
  let points = [];

  planePoints.forEach((panelPoint) => {
    points.push(new THREE.Vector3(panelPoint[0], panelPoint[1], panelPoint[2]));
  });

  material = new THREE.LineBasicMaterial({ color: "blue" });
  meshGeometry = new THREE.ConvexGeometry( points ); // points = vertices array
  mesh = new THREE.Mesh(meshGeometry, material);
  mapScene.add(mesh);
}

/*
*
* scan plane data example
* {
*   angle: float
*   x_offset: float
*   y_offset: float
*   width: float
*   distance: float
*   time: int
* }
*
*/
const round = num => Math.round(num * 100) / 100;

const rotatePlane = (angle, planeVertices) => {
  const new_coords = [];
  const rad = degToRad(angle)

  planeVertices.forEach(planeVertice => {
    new_coords.push([
      round((planeVertice[0] * Math.cos(rad)) - (planeVertice[1] * Math.sin(rad))),
      round((planeVertice[1] * Math.cos(rad)) + (planeVertice[0] * Math.sin(rad)))
    ]);
  });

  return new_coords;
};

const getPlaneVertices = (angle, plane) => {
  const planeVertices = [
    [plane.x_offset,               plane.y_offset],
    [plane.x_offset + plane.width, plane.y_offset],
    [plane.x_offset + plane.width, plane.y_offset + plane.distance],
    [plane.x_offset,               plane.y_offset + plane.distance]
  ];

  if (angle) {
    const rotatedPlaneVertices = rotatePlane(angle, planeVertices);
    return rotatedPlaneVertices;
  }

  return planeVertices;
};

const scanPlane = (angle, x_offset, y_offset, width, distance, time) => ({
  angle,
  x_offset,
  y_offset,
  width,
  distance,
  time
});

const fullScanPlanes = (angle, x_offset, y_offset, time) => {
  const imu_z = 0.58; // forward

  plotFourPointsAsPlane(
    getPlaneVertices(
      angle, scanPlane(angle, x_offset, y_offset + imu_z,        4.6, 1.69, time)
    )
  );

  plotFourPointsAsPlane(
    getPlaneVertices(
      angle, scanPlane(angle, x_offset, y_offset + imu_z + 1.69, 10, 6.35, time)
    )
  );

  plotFourPointsAsPlane(
    getPlaneVertices(
      angle, scanPlane(angle, x_offset, y_offset + imu_z,        -4.6, 1.69, time)
    )
  );

  plotFourPointsAsPlane(
    getPlaneVertices(
      angle, scanPlane(angle, x_offset, y_offset + imu_z + 1.69, -10, 6.35, time)
    )
  );
};

const plotFullScanPlane = (angle, x_offset, y_offset) => {
  
};

// 360 scan
// fullScanPlanes(0, 0, 0, 0);
// fullScanPlanes(90, 0, 0, 0);
// fullScanPlanes(180, 0, 0, 0);
// fullScanPlanes(270, 0, 0, 0);

// move forward 20", scan 360
// fullScanPlanes(0, 0, 20, 0);
// fullScanPlanes(90, 20, 0, 0);
// fullScanPlanes(180, 0, -20, 0);
// fullScanPlanes(270, -20, 0, 0);

const plotSinglePlane = (angle, x_offset, y_offset, width, distance) => {

};
