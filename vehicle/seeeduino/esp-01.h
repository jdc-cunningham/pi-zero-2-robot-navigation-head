#define ESPSERIAL Serial1

String curEspMsg = "";
String motionCommand = "rc_084_098_1400";

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
    return ESPSERIAL.readString();
  }

  return "";
}

void checkMessages()
{
  // poll is like a keep-alive, it bunches up due timing mismatch
  String espMsg = getEspSerialMsg();
  
  if (espMsg)
  {
    // espMsg.replace("", "");
  }

  if (espMsg)
  {
    motionCommand = espMsg;
    clearEspSerial();
  }
  
  delay(50);
}
