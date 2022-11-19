// sample coordiantes facing a wall
// 10 - [39.86, 33.91, 34.12, 33.91, 33.87, 34.11, 34.25, 34.59, 34.47, 35.24, 35.68, 39.99, 41.19]
// 0 - [24.38, 34.18, 33.98, 34.19, 33.99, 34.29, 34.15, 34.35, 34.66, 34.89, 39.42, 39.49, 39.63]
// -10 - [35.44, 34.29, 34.07, 34.45, 34.08, 34.25, 34.25, 34.35, 34.81, 35.79, 39.71, 40.01, 39.86]
// -20 - [40.24, 34.72, 34.97, 34.5, 34.84, 34.99, 34.71, 34.82, 35.44, 39.61, 40.73, 40.45, 41.13]

// inclineAngle - abs value
// sweepAngle 
// inches
// flip in case of values measured below sensor horizon
// x, y, z coordinate system where z faces user
const get3dCoordinates = (inclineAngle, sweepAngle, measurement, flip) => {
	const xCoord = measurement * Math.sin(sweepAngle);
  const yCoord = inclineAngle === 0 ? 0 : (measurement * Math.cos(inclineAngle) * (flip ? -1 : 1));
  const zCoord = measurement * Math.cos(sweepAngle);
  return [xCoord, yCoord, zCoord];
};

// since pan/tilt ranges limited by 30 deg in either dir
const angleMap = [
  -10,
  0,
  10,
];

// 45 deg sample, max/diag is 14", 13" 10deg left/right approx

// center, center of pan, tilt is technically 0,0 but it is above the horizon regarding the sensor/robot position
const measuredCoordinates =  [
  [14.2, 14.4, 14.79],
  [14.33, 14.27, 14.44],
  [14.54, 14.22, 10.89]
];

const coordinates = measuredCoordinates.map((row, index) => {
  // console.log(row);
  return row.map((measurement, rowIndex) => get3dCoordinates(
    angleMap[index],
    angleMap[rowIndex],
    measurement,
   	index > 1,
  ));
});

/* console.log(coordinates.join(",")); */
// console.log(coordinates);