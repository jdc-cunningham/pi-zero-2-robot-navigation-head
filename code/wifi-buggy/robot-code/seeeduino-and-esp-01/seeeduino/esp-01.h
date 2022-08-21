#define ESPSERIAL Serial1

// used to avoid buffer buildup between ESP and web communication delay
String curEspMsg = "";

void setupEspSerial()
{
  ESPSERIAL.begin(115200);
}

void clearEspSerial()
{
  while (ESPSERIAL.available() > 0)
  {
    ESPSERIAL.read();
  }
}

String getEspSerialMsg() {
  if (ESPSERIAL.available() > 0) {
    String msg = ESPSERIAL.readString();
    return msg;
  }

  return "";
}

void writeToEsp(String msg)
{
  if (curEspMsg.length() == 0)
  {
    curEspMsg = msg;
    ESPSERIAL.print(msg);
    ESPSERIAL.flush();
    curEspMsg = "";
  } else
  {
    Serial.println("esp write err");
  }
}

String getUnitFromStr(String msg, String msgStart, String msgEnd)
{
  int startIndex = msg.indexOf(msgStart) + 5; // eg. _mfs_
  int endIndex = msg.indexOf(msgEnd);

  return msg.substring(startIndex, endIndex);
}

void checkMessages()
{
  // poll is like a keep-alive, it bunches up due timing mismatch
  String espMsg = getEspSerialMsg();
  
  if (espMsg)
  {
    espMsg.replace("poll", "");
    espMsg.replace("Hello Server!", "");
  }

  if (espMsg)
  {
    Serial.println(espMsg);

    // the motion command comes in like _mfs_10_mfe_ which means move forward 10 inches
    // the command is stripped and the unit, then you turn that into degrees to rotate
    // based on diameter of the robot wheels (5 inches)

    // going to use a pattern like command start/end
    // eg. mfs_ val _ mfe just for known start/end points
    // due to serial build up transmitted by websocket = bad code
    // indexOf is due to chunking
    if (espMsg.indexOf("_mfs_") > -1 && espMsg.indexOf("_mfe_") > -1)
    {
      activeDirection = "forward";
      Serial.println(espMsg);
      motionVal = getUnitFromStr(espMsg, "_mfs_", "_mfe_").toInt();
      maxMotionVal = getDegreesFromInches(motionVal);
      Serial.println(espMsg);
      Serial.println(motionVal);
      Serial.println(maxMotionVal);
    }

    if (espMsg.indexOf("_mls_") > -1 && espMsg.indexOf("_mle_") > -1)
    {
      activeDirection = "left";
      motionVal = getUnitFromStr(espMsg, "_mls_", "_mle_").toInt();
      int inchesToMove = getInchesFromAngle(motionVal);
      maxMotionVal = getDegreesFromInches(inchesToMove);
    }

    if (espMsg.indexOf("_mrs_") > -1 && espMsg.indexOf("_mre_") > -1)
    {
      activeDirection = "right";
      motionVal = getUnitFromStr(espMsg, "_mrs_", "_mre_").toInt();
      int inchesToMove = getInchesFromAngle(motionVal);
      maxMotionVal = getDegreesFromInches(inchesToMove);
    }

    if (espMsg.indexOf("_mbs_") > -1 && espMsg.indexOf("_mbe_") > -1)
    {
      activeDirection = "back";
      motionVal = getUnitFromStr(espMsg, "_mbs_", "_mbe_").toInt();
      maxMotionVal = getDegreesFromInches(motionVal);
    }

    if (espMsg.indexOf("m_s") > -1)
    {
      activeDirection = "";
    }

    if (espMsg.indexOf("m_r360") > -1)
    {
      activeDirection = "r360";
      motionVal = 19;
      maxMotionVal = 22;
    }

    clearEspSerial();
  }

  // Serial.println("check");

  delay(250); // delay for sync
}
