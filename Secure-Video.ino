// Certificates (should be replaced with actual certificates)
const char* cert = "MIIDszCCApsCFCgdjZItAXHeEWD2+SAqIjD2fi3mMA0GCSqGSIb3DQEBCwUAMIGV\n"
                   "MQswCQYDVQQGEwJJTjELMAkGA1UECAwCVE4xEDAOBgNVBAcMB1ZlbGxvcmUxETAP\n"
                   "BgNVBAoMCHdlZG90aGlzMRkwFwYDVQQLDBB3ZWRvdGhpc3Byb2plY3QxMREwDwYD\n"
                   "VQQDDAh2aWRlby5pbjEmMCQGCSqGSIb3DQEJARYXb3BlcmF0aW9ub3dsNEBnbWFp\n"
                   "bC5jb20wHhcNMjQxMTA3MTY1MTU5WhcNMjUxMTA3MTY1MTU5WjCBlTELMAkGA1UE\n"
                   "BhMCSU4xCzAJBgNVBAgMAlROMRAwDgYDVQQHDAdWZWxsb3JlMREwDwYDVQQKDAh3\n"
                   "ZWRvdGhpczEZMBcGA1UECwwQd2Vkb3RoaXNwcm9qZWN0MTERMA8GA1UEAwwIdmlk\n"
                   "ZW8uaW4xJjAkBgkqhkiG9w0BCQEWF29wZXJhdGlvbm93bDRAZ21haWwuY29tMIIB\n"
                   "IjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiQkGr0FtVrjAQ3NpILcfmghS\n"
                   "2dZblGUK5LMnVxZ/It4fVxgjWZRTv3COBs371sRrLBBCYW5gEc6Xt/QE//zhFFTX\n"
                   "p1MGtwGGaRtud6Zgo8PNadogPDEGKjUe1CNM+g1AoFvjL8M/TblEuilrA21lmbuT\n"
                   "j+m5cXRLyxmBcXG/vec7HbHFK0GLs4wstR0ixfZwkJRNA+lgo2CwCI2WoKjB+Zjp\n"
                   "ciQdFqwnex8D2oA+bf5L3IZl1vUg4TkxyiDyHw2gedndO0A8K1Ulwyc4BOCSwQlO\n"
                   "qOfHLwVmgGmTZjA9srSxIOLlGTzotaW1CHSXTai27nvoFcPO3TYu9b5UjW629QID\n"
                   "AQABMA0GCSqGSIb3DQEBCwUAA4IBAQAu218H7GqedI0hPSWQMoMtXwBILJhj2u2i\n"
                   "brVgj0dg0ZSwumj11N8CcfRPGM07AkBC8R8eRj4mMF1+pRp4E6O18DxWPzXmURpk\n"
                   "1OFEy1Izzdlw8zHgg4x7qyrrrAQyx21V/2yByVo5e5LOPZCF54+/W3HUrTXSRRfp\n"
                   "n3OQod8a1ZNERfrzpLZzhfWpIpQz93i0ucWTncRywej67ZIOveKR6tYztlkhbcY0\n"
                   "voc25zQ1YNYNqP1VxPwJTPH9lk8yV11g3W3wbJ6OXZAyDC3vUk9aG/5IgfY7kx8v\n"
                   "DG3COj7wxy+XVqRlJ9+Ng0uHte4AM6XjxtVwfqoN3++LjdJU19li\n";

const char* privateKey = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCJCQavQW1WuMBD\n"
                         "c2kgtx+aCFLZ1luUZQrksydXFn8i3h9XGCNZlFO/cI4GzfvWxGssEEJhbmARzpe3\n"
                         "9AT//OEUVNenUwa3AYZpG253pmCjw81p2iA8MQYqNR7UI0z6DUCgW+Mvwz9NuUS6\n"
                         "KWsDbWWZu5OP6blxdEvLGYFxcb+95zsdscUrQYuzjCy1HSLF9nCQlE0D6WCjYLAI\n"
                         "jZagqMH5mOlyJB0WrCd7HwPagD5t/kvchmXW9SDhOTHKIPIfDaB52d07QDwrVSXD\n"
                         "JzgE4JLBCU6o58cvBWaAaZNmMD2ytLEg4uUZPOi1pbUIdJdNqLbue+gVw87dNi71\n"
                         "vlSNbrb1AgMBAAECggEAQbUWw/Uy2Njos88Ekx/Lot+n3nUW335drVCsJemPF6h7\n"
                         "TZcw6BSj3ZE6QNAHGDGBlBTNx4sVvKQbgqSauyZFxKpz53L7rsen7AEvxGZ+Qzgx\n"
                         "aDajq0j0hEuJVz3//IxbNykoM/BCi+GwrzUJ75BGneLf/CsddOXHLAE0XLGmt4cT\n"
                         "ZavnST4hoB4+kjPgJXMTnu+zazDl4LMa2b03rXXqoHZRwtr36GtBZEhcawaAeCHy\n"
                         "pAUfpyJ7kMr2kUujp2qaCOLqU+h2liZ5rBVCU5r0Fracb9Y7hWduEy9TJ/8L6i4L\n"
                         "6tp1ViUYwgEyhY5IV+jn0GcINm/R2FbgfieiAwbF5wKBgQC8S8yp78tP7j9YZCyI\n"
                         "WB1BOtHOtUPxwbkD2odgMCL5Q2bkWqTcCrl66ImQuabZp3q9072p1M7Kaz12vOnh\n"
                         "rspWb35a77LYyDAuZ+G4MAmGQ+ABmHIxMsOPsMEyZ14z/mgvBEpEfQXOcnoz3RWh\n"
                         "yOkPVuHAv9vDOcHnybTL5j4/RwKBgQC6TspsPnoLBRvUpHh0pq02qrBFVNbM6F4q\n"
                         "jLoVjgEJM1FtS+O16+b+WdyVWkyNgcQjXC+ZVrzpgM05L526GOfelo0YU6bRTqWz\n"
                         "8ZVS2wqT9LObcC76J1xbLcVm8Z0CSPkVR3r+LyuxtpxEsiDGA8JEkquzRs1y6iGr\n"
                         "cW2dy8oN4wKBgC7hfHJvBqK/AbyDLGdB8P61o1kg3mrJvcPM29nCAmMnOe3u947l\n"
                         "iKqmTOHgpz8XqMKsflNTba0OKD5w6JZNC4mbtszzUwcQSJa1PIi8RRLNwW8EQqIn\n"
                         "LnOPIXroK5csZ0oVelw0+IYfEHfrOqCOQiCUlB6GZjPkJHgOS1pc1/CvAoGBAJ/u\n"
                         "sUAYpeW93fU9txXUW09ZWXY67SX7t5JpOfj07Ri70AO2KOTrfGEOPRiM6rhzFC+S\n"
                         "nF3SotsEMagMoya06J8guECQ1txI2mBNW3VECaGXZ3Ng60Lc9SBke1fyw2jJweEt\n"
                         "enyne6fT7fPewdmaMnNxQSnl9snWCU9GUOYroeknAoGAYA5CG160NlkKsvp0bK7Q\n"
                         "m1vm020mND+qm+5/NrtooVA5T2BrndKN7HVUUybVIcWBbXWx3D6UMVV3t5oxCPRC\n"
                         "4xpNrRvWY8anMM044Pl+EBs1Xl698Z4HwDth4Fs2tlqIVhFIQkLFRT7oHvWajBwa\n"
                         "S4gYpo13Xd5EFrl0yZjP7i0=\n";

#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoWebsockets.h>

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

// WebSocket server on port 81 (secure WebSocket)
websockets::WebSocketServer webSocketServer;

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
  config.frame_size = FRAMESIZE_SVGA; // Options: FRAMESIZE_VGA, FRAMESIZE_XGA, FRAMESIZE_SVGA, etc.
  config.jpeg_quality = 13;           // Lower value means higher quality (0-63)
  config.fb_count = 3;                // Increase frame buffer count for smoother streaming

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    return;
  }
  Serial.println("Camera init succeeded");

  // Access the camera sensor and set contrast, saturation, and brightness
  sensor_t* s = esp_camera_sensor_get();
  if (s) {
    s->set_contrast(s, 2);     // Set contrast to 2
    s->set_saturation(s, 1);  // Set saturation to -2
    s->set_sharpness(s, 1);    // Improve sharpness for better detail
  }
}

// WebSocket event handler
void onEvent(websockets::WebSocket &socket, websockets::WebSocketEvent event, String &data) {
  if (event == websockets::WebSocketEvent::ConnectionOpened) {
    Serial.println("Client connected.");
  } else if (event == websockets::WebSocketEvent::ConnectionClosed) {
    Serial.println("Client disconnected.");
  }
}

// Stream the camera frames to WebSocket clients
void streamCamera() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (fb) {
    // Broadcast the frame to all clients
    webSocketServer.broadcastBinary(fb->buf, fb->len);
    esp_camera_fb_return(fb); // Return the frame buffer
  } else {
    Serial.println("Camera capture failed");
  }
}

void setup() {
  Serial.begin(115200);
  
  // Initialize SPIFFS for storing files (if needed)
  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS Mount Failed");
    return;
  }
  
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
  
  // Create an SSL WiFiClientSecure
  WiFiClientSecure secureClient;
  secureClient.setCertificate(server_cert);
  secureClient.setPrivateKey(server_key);

  // Start the WebSocket server with SSL
  webSocketServer.begin(secureClient, 81);
  webSocketServer.onEvent(onEvent);
  Serial.println("Secure WebSocket server started");
}

void loop() {
  webSocketServer.poll();  // Handle WebSocket events
  streamCamera();          // Capture and send frames to clients
  delay(50);               // Adjust this delay for controlling frame rate (increased smoothness)
}

