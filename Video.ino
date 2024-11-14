#include "esp_camera.h"
#include <WiFi.h>
#include <WebSocketsServer.h>

// Replace with your network credentials
const char* ssid = "Dododo";
const char* password = "Dodododo";

// Camera model pin configuration for AI-Thinker
#define CAMERA_MODEL_AI_THINKER

#define PWDN_GPIO_NUM  32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  0
#define SIOD_GPIO_NUM  26
#define SIOC_GPIO_NUM  27

#define Y9_GPIO_NUM    35
#define Y8_GPIO_NUM    34
#define Y7_GPIO_NUM    39
#define Y6_GPIO_NUM    36
#define Y5_GPIO_NUM    21
#define Y4_GPIO_NUM    19
#define Y3_GPIO_NUM    18
#define Y2_GPIO_NUM    5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM  23
#define PCLK_GPIO_NUM  22

// LED Pin (optional, use GPIO 4 for flash or 33 for normal LED)
#define LED_GPIO_NUM   4

// Create a WebSocket server on port 81
WebSocketsServer webSocket = WebSocketsServer(81);

// Start the camera
void startCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // Set higher resolution and better JPEG quality
  config.frame_size = FRAMESIZE_VGA; // Options: FRAMESIZE_VGA, FRAMESIZE_XGA, FRAMESIZE_SVGA, etc.
  // config.frame_size = FRAMESIZE_HD; // Options: FRAMESIZE_VGA, FRAMESIZE_XGA, FRAMESIZE_SVGA, FRAMESIZE_HD, etc.
  config.jpeg_quality = 7;           // Lower value means higher quality (0-63)
  config.fb_count = 3;                // Increase frame buffer count for smoother streaming

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    return;
  }
  Serial.println("Camera init succeeded");

  // Access the camera sensor and set contrast, saturation, and brightness
  sensor_t* s = esp_camera_sensor_get();
  // if (s) {
    // s->set_contrast(s, 2);     // Set contrast to 2
    // s->set_saturation(s, 2);  // Set saturation to -2
    // s->set_sharpness(s, 1);    // Improve sharpness for better detail
  // }
}

// WebSocket event handler
void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED) {
    Serial.printf("Client %u connected\n", num);
  } else if (type == WStype_DISCONNECTED) {
    Serial.printf("Client %u disconnected\n", num);
  }
}

// Stream the camera frames to WebSocket clients
void streamCamera() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (fb) {
    webSocket.broadcastBIN(fb->buf, fb->len); // Send the captured frame as binary data to all clients
    esp_camera_fb_return(fb); // Return the frame buffer
  } else {
    Serial.println("Camera capture failed");
  }
}

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  
  // Start the camera
  startCamera();
  
  // Start the WebSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  Serial.println("WebSocket server started");
}

void loop() {
  webSocket.loop(); // Handle WebSocket client connections
  streamCamera();   // Capture and send frames to clients
  delay(50);        // Adjust this delay for controlling frame rate (increased smoothness)
}
