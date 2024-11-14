#include "DHT.h"

#define DHTPIN 19     // Digital pin connected to the DHT sensor
#define D0_PIN 15     // Digital output pin from MQ-2 connected to GPIO 15
#define A0_PIN 14      // Analog output pin from MQ-2 connected to GPIO D2 (Analog GPIO 4)

int gasAnalogValue = 0;   // Variable to store analog gas value
int disconnectThreshold = 10; // Threshold to detect disconnection (near-zero value)


#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));
  pinMode (18, OUTPUT);
  pinMode (21, OUTPUT);
  digitalWrite(18, HIGH);
  digitalWrite(21, LOW);
  pinMode(A0_PIN, INPUT);
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  gasAnalogValue = analogRead(A0_PIN);
  if (gasAnalogValue < disconnectThreshold) {
    Serial.println("Warning: Gas sensor appears to be disconnected!");
  } else {
    // Display the gas concentration value
    Serial.print("Gas Concentration: ");
    Serial.println(gasAnalogValue);
  }

  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));
}
