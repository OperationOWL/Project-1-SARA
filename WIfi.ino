#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>
#include "DHT.h"

#define DHTPIN 13     // Digital pin connected to the DHT sensor
#define A0PIN 33      // Analog output pin from MQ-2 connected to GPIO D2 (Analog GPIO 4)

#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

int gasAnalogValue = 0;   // Variable to store analog gas value
int disconnectThreshold = 10; // Threshold to detect disconnection (near-zero value)

// Network credentials
const char* ssid = "Dododo";
const char* passwd = "Dodododo";

WebServer httpServer(80);
WebSocketsServer webSocket(81); // WebSocket server runs on port 81

String readGasData() {
  gasAnalogValue = analogRead(A0PIN); // Read the analog value from the sensor
  if (gasAnalogValue < disconnectThreshold) {
    return String("Gas: -1");  // Returning gas data in the format "gas: -1" if disconnected
  } else {
    return String("Gas: " + String(gasAnalogValue));  // Send the gas level
  }
}

String readDHTData() {
    float h = dht.readHumidity();  // Read humidity
    float t = dht.readTemperature();  // Read temperature in Celsius
    float f = dht.readTemperature(true);  // Read temperature in Fahrenheit

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t) || isnan(f)) {
        return String("Failed DHT!"); // Return error message
    }

    // Compute heat index in Fahrenheit
    float hif = dht.computeHeatIndex(f, h);
    // Compute heat index in Celsius
    float hic = dht.computeHeatIndex(t, h, false);

    // Create output string in the format: "humidity: xx, temp: xx.x, heat_index: xx.x"
    String output = "Humidity: " + String(h) + ", Temp: " + String(t) + ", HI: " + String(hic);
    return output;  // Return the formatted string
}

// Handle new WebSocket connections
void webSocketEvent(uint8_t clientNum, WStype_t type, uint8_t *payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.printf("Client %u disconnected\n", clientNum);
      break;
    case WStype_CONNECTED:
      Serial.printf("Client %u connected\n", clientNum);
      break;
    case WStype_TEXT:
      payload[length] = 0; // Null-terminate the string for printing
      Serial.printf("Message from client %u: %s\n", clientNum, payload);
      break;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(DHTPIN, INPUT);
  pinMode(A0PIN, INPUT);
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  dht.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, passwd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print the IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start WebSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent); // Use the corrected function signature
  
  // Print confirmation when WebSocket has started
  Serial.println("WebSocket server started on port 81");
}


void loop() {
  // Handle WebSocket connections
  String gasData;
  webSocket.loop();

  // Check Wi-Fi connection status
  static bool lastConnectionState = true;
  bool currentConnectionState = (WiFi.status() == WL_CONNECTED);

  if (currentConnectionState != lastConnectionState) {
    if (currentConnectionState) {
      Serial.println("WiFi reconnected");
    } else {
      Serial.println("WiFi disconnected");
    }
    lastConnectionState = currentConnectionState;
  }

  // You can send periodic updates to all connected clients
  // This is just an example of sending data every 250 ms
  static unsigned long lastSendTime = 0;
  if (millis() - lastSendTime > 250) {
    lastSendTime = millis();
    String gasData = readGasData();
    String dhtData = readDHTData();
    
    // Combine all sensor data into one formatted string
    String fullData = gasData + ", " + dhtData;  // Create a single message

    // Send the combined data to all connected clients
    webSocket.broadcastTXT(fullData);
  }
}
