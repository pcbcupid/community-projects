#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WebSocketsServer.h>
#include <TM1637Display.h>

const char* ssid = "your_ssid";
const char* password = "your_passwd";

// web_socket on port 81
WebSocketsServer webSocket = WebSocketsServer(81);

#define CLK 5
#define DIO 4

TM1637Display display(CLK, DIO);

// it will handle incoming vals from web_Socket
void handleWebSocketMessage(void* arg, uint8_t* data, size_t len) {
  String message = "";
  for (size_t i = 0; i < len; i++) {
    message += (char)data[i];
  }

  int brightness = message.toInt();
  brightness = constrain(brightness, 0, 255);

  display.showNumberDec(brightness, false);

  // display_brightness control
  int dispBrightness = map(brightness, 0, 255, 0, 7);
  display.setBrightness(dispBrightness);

  Serial.print("Received Brightness: ");
  Serial.println(brightness);
}

void onEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_TEXT) {
    handleWebSocketMessage(nullptr, payload, length);
  }
}

void setup() {
  Serial.begin(115200);
  display.setBrightness(7);  

  // connect the almighty wi-fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // start web_socket
  webSocket.begin();
  webSocket.onEvent(onEvent);
}

void loop() {
  webSocket.loop();
}
