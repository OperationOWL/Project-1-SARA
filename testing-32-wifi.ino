#include <WiFi.h>
#include <WebSocketsServer.h>

// Network credentials
const char* ssid = "Dododo";
const char* password = "Dodododo";

// WebSocket server on port 81
WebSocketsServer webSocket = WebSocketsServer(81);

// Handle incoming WebSocket messages
void webSocketEvent(uint8_t clientNum, WStype_t type, uint8_t *payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.printf("Client %u disconnected\n", clientNum);
      break;
    case WStype_CONNECTED: {
      IPAddress ip = webSocket.remoteIP(clientNum);
      Serial.printf("Client %u connected from %s\n", clientNum, ip.toString().c_str());
      webSocket.sendTXT(clientNum, "Welcome to the ESP32 WebSocket server!");
      break;
    }
    case WStype_TEXT:
      Serial.printf("Received message from client %u: %s\n", clientNum, payload);
      // Echo the message back to the client
      webSocket.sendTXT(clientNum, payload);
      break;
    default:
      break;
  }
}

void setup() {
  // Start Serial Monitor
  Serial.begin(9600);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start WebSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  Serial.println("WebSocket server started on port 81");
}

void loop() {
  // Handle WebSocket events
  webSocket.loop();
}
