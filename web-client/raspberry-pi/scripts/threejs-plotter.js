// this has to be hosted somewhere, in my case a Raspberry Pi Apache Web Server
// needs CORS
const baseGlbPath = "http://192.168.1.144/3d-files/";
const robotGlbFilename = "basic-robot-model.glb";
const loader = new THREE.GLTFLoader();
const gltfs = {};
const scene = new THREE.Scene();

const degToRad = (deg) => deg * 0.0174533;

const threejsPlotChart = () => {
  // https://threejs.org/docs/#manual/en/introduction/Creating-a-scene
  THREE.Object3D.DefaultUp.set(0, 0, 1); // set Z as vertical axes
  // 10 z distanece
  const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 2000);
  const canvas = document.getElementById("threejs-canvas");
  const renderer = new THREE.WebGLRenderer({ canvas: canvas }); // https://stackoverflow.com/a/21646450/2710227
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
  const size = 5;
  const divisions = 20;
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

        console.log(gltf);

        scene.add(new THREE.AmbientLight(0xdddddd)); // controls brightness of colors
        // gltf.scene.position.x=10
        scene.add( gltf.scene );

        gltf.animations; // Array<THREE.AnimationClip>
        gltf.scene; // THREE.Group
        gltf.scenes; // Array<THREE.Group>
        gltf.cameras; // Array<THREE.Camera>
        gltf.asset; // Object

        renderer.render( scene, camera );
        gltfs["basic-robot-model"].handle.scene.rotateX(degToRad(90)); // match blue as Z axis
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
