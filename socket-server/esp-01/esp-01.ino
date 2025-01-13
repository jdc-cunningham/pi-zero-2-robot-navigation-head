// using library https://github.com/gilmaimon/ArduinoWebsockets
#include <ArduinoWebsockets.h>
#include <ESP8266WiFi.h>

using namespace websockets;
WebsocketsServer socketServer;

bool clientActive = false;

void connectToWiFi()
{
  WiFi.begin("SSID", "PASS");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  socketServer.listen(80);
}

void setup()
{
  Serial.begin(115200);
  connectToWiFi();
} 

void loop()
{
  if (!clientActive)
  {
    auto client = socketServer.accept();
    clientActive = true;

    // 1 second ESP to Web client connection poll
    for (int i = 0; i < 200; i++)
    {
      if (client.available())
      {
        auto msg = client.readBlocking();

        if (msg.data().length() > 0)
        {
          Serial.print(msg.data());
        }

        if (Serial.available() > 0)
        {
          client.send(Serial.readString());
          Serial.flush(); // this does nothing
        }
      }
      delay(50);
    }

    client.close();
    clientActive = false;
  }

  delay(50);
}