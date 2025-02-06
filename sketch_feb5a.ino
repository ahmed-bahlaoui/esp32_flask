#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your network credentials
const char* ssid = "esp32_dev";
const char* password = "12345678";

// Replace with your Flask server IP and endpoint
const char* serverUrl = "http://192.168.143.209:5000/upload";

// Camera configuration for AI Thinker ESP32-CAM
#define PWDN_GPIO_NUM    32
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM     0
#define SIOD_GPIO_NUM    26
#define SIOC_GPIO_NUM    27
#define Y9_GPIO_NUM      35
#define Y8_GPIO_NUM      34
#define Y7_GPIO_NUM      39
#define Y6_GPIO_NUM      36
#define Y5_GPIO_NUM      21
#define Y4_GPIO_NUM      19
#define Y3_GPIO_NUM      18
#define Y2_GPIO_NUM       5
#define VSYNC_GPIO_NUM   25
#define HREF_GPIO_NUM    23
#define PCLK_GPIO_NUM    22

void setup() {
  Serial.begin(115200);

  // Initialize the camera
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

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA; // Use UXGA (1600x1200)
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA; // Use SVGA (800x600)
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Initialize the camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void loop() {
  // Check if the server requests a picture
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl); // Specify the URL of the Flask endpoint
    http.addHeader("Content-Type", "image/jpeg");

    // Capture a photo
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      return;
    }

    // Send the photo to the server
    int httpResponseCode = http.POST((uint8_t *)fb->buf, fb->len);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.printf("HTTP Response code: %d\n", httpResponseCode);
      Serial.println(response);
    } else {
      Serial.printf("Error in HTTP POST: %d\n", httpResponseCode);
    }

    // Free the frame buffer
    esp_camera_fb_return(fb);
    http.end();
  }
  delay(5000); // Wait before taking another picture
}