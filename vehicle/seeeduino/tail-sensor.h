// based on this library 
// https://github.com/Seeed-Studio/Seeed_Arduino_AS5600
#include <Wire.h>
#include <AS5600.h>

#ifdef ARDUINO_SAMD_VARIANT_COMPLIANCE
  #define SYS_VOL   3.3
#else
  #define SYS_VOL   5
#endif

AMS_5600 ams5600;

int ang, lang = 0;

void setupTailSensor()
{
  Wire.begin();

  if(ams5600.detectMagnet() == 0)
  {
    while (1)
    {
      if (ams5600.detectMagnet() == 1 )
      {
        Serial.print("Current Magnitude: ");
        Serial.println(ams5600.getMagnitude());
        break;
      }
      else
      {
        Serial.println("Can not detect magnet");
      }

      delay(1000);
    }
  }
}

/*******************************************************
 * Function: convertRawAngleToDegrees
 * In: angle data from AMS_5600::getRawAngle
 * Out: human readable degrees as float
 * Description: takes the raw angle and calculates
 * float value in degrees.
 *******************************************************/
float convertRawAngleToDegrees(word newAngle)
{
  /* Raw data reports 0 - 4095 segments, which is 0.087890625 of a degree */
  float retVal = newAngle * 0.087890625;

  return retVal;
}
