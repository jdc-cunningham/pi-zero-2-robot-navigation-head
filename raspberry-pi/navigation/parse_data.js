const table = document.getElementById("table");

const black_mat_1 = [
  [[9.55, 9.52, 9.2, 8.74], [9.71, 9.63, 9.24, 8.97]],
  [[12.71, 12.44, 12.05, 11.51, 11.12], [12.71, 12.83, 12.56, 12.17, 11.66]],
  [[31.98, 29.09, 25.0, 21.45], [32.21, 30.69, 25.9]]
];

const black_mat_2 = [
  [[9.24, 9.24, 8.97, 8.58], [9.4, 9.36, 9.09, 8.85]],
  [[12.13, 11.89, 11.51, 11.12, 10.69], [12.44, 12.29, 12.29, 11.97, 11.66]],
  [[31.28, 27.38, 23.28, 23.4], [29.6, 27.18, 24.53]]
];

const brown_carpet_1 = [
  [[9.17, 9.09, 8.78, 8.46], [9.32, 9.4, 9.2, 8.93]],
  [[12.05, 11.66, 11.39, 11.08, 10.69], [12.21, 12.56, 12.36, 12.09, 11.74]],
  [[34.12, 32.64, 24.84, 21.61], [31.08, 29.05, 26.79]]
];

const brown_carpet_2 = [
  [[9.13, 9.09, 8.74, 8.42], [9.2, 9.4, 9.2, 8.85]],
  [[12.09, 11.7, 11.23, 10.8, 10.53], [12.29, 12.36, 12.48, 12.05, 11.54]],
  [[33.46, 31.9, 24.45, 21.68], [29.8, 29.37, 26.48]]
];

const wooden_floor_1 =[
  [[10.06, 9.67, 9.55, 8.97], [10.06, 9.71, 9.71, 9.28]],
  [[12.99, 12.56, 12.21, 11.93, 11.35], [12.99, 12.91, 12.71, 12.75, 12.25]],
  [[319.41, 319.45, 319.45, 319.45], [319.45, 36.15, 25.04]]
];

const wooden_floor_2 = [
  [[9.59, 9.48, 9.4, 9.13], [9.91, 10.22, 9.75, 9.32]],
  [[13.42, 12.99, 12.56, 11.66, 11.19], [13.03, 13.42, 12.87, 12.17, 11.7]],
  [[319.41, 319.45, 319.45, 319.45], [319.41, 319.45, 27.26]]
];

const all_data = {
	"black_mat_1": black_mat_1,
  "black_mat_2": black_mat_2,
  "brown_carpet_1": brown_carpet_1,
  "brown_carpet_2": brown_carpet_2,
  "wooden_floor_1": wooden_floor_1,
  "wooden_floor_2": wooden_floor_2
 };

let printSet = [
	[[], []],
  [[], []],
  [[], []]
];

const map = new Map();

let activeIndex = 0;
let largestVal = 0;

Object.keys(all_data).forEach((key, index) => {
	all_data[key].forEach((tilt, index2) => { // tilt
  	tilt.forEach((sweep, index3) => { // sweep
    	sweep.forEach((sensor, index4) => { // sensor value
        if (index == 0) printSet[index2][index3][index4] = [];
        printSet[index2][index3][index4].push(sensor);
        
        if (sensor > largestVal && sensor < 300) {
        	largestVal = sensor;
        }
      });
      
      largestVal = 0;
    });
  });
});

const avgSensorDepths = [
	[[], []],
  [[], []],
  [[], []]
];

console.log(printSet);

printSet.forEach((tilt, index1) => {
  tilt.forEach((sweep, index2) => {
  	let sensorAvg = 0;
    
    sweep.forEach((sensor, index3) => {
      sensorAvg = Math.round((sensor.reduce((a, b) => a + b) / sensor.length) * 100) / 100;
      avgSensorDepths[index1][index2][index3] = sensorAvg;
    });
  });
});

console.log(avgSensorDepths);
