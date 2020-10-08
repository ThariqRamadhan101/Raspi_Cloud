#include "WiFi.h"
#include "esp_camera.h"
#include <PubSubClient.h>

/* MQTT Credentials */
#define MQTT_USERNAME     "dimyog7@gmail.com"
#define MQTT_KEY          "demoesp32"
#define MQTT_TOPIC        "dimyog7@gmail.com/demo"
#define MQTT_BROKER       "maqiatto.com"
#define MQTT_BROKER_PORT  1883

/* WiFi Credentials */
#define WIFI_SSID "susahbanget"
#define WIFI_PASSWORD "susahbanget"

/*Camera Pin*/
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

WiFiClient wf_client;
PubSubClient client(wf_client);

camera_fb_t * fb = NULL;
unsigned long last;

bool camera_init(){
  // IF USING A DIFFERENT BOARD, NEED DIFFERENT PINs
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

  //init with high specs to pre-allocate larger buffers
  config.frame_size   = FRAMESIZE_VGA; // set picture size, FRAMESIZE_QQVGA = 160x120
  config.jpeg_quality = 10;            // quality of JPEG output. 0-63 lower means higher quality
  config.fb_count     = 1;

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK)
  {
    Serial.print("Camera init failed with error 0x%x");
    Serial.println(err);
    return false;
  }

  // Change extra settings if required
  //sensor_t * s = esp_camera_sensor_get();
  //s->set_vflip(s, 0);       //flip it back
  //s->set_brightness(s, 1);  //up the blightness just a bit
  //s->set_saturation(s, -2); //lower the saturation

  else
  {
    return true;
  }
  
}

void reconnect() {
  // Loop until we're reconnected
  bool sending = false;

  while ((!client.connected()) || (!sending)) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("esp32cam", MQTT_USERNAME, MQTT_KEY)) {
      Serial.println("connected");
      
      fb = esp_camera_fb_get();
      if(fb){
        Serial.print("img size: ");
        Serial.print(fb->len);
        Serial.println(" B");
        client.publish(MQTT_TOPIC, (const uint8_t *)(fb->buf), fb->len);
        sending = true;
        Serial.println("image send success");
      }else{
        Serial.println("Camera capture failed");
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup(){
  Serial.begin(9600);

  while(!camera_init()){
    Serial.println("Failed to initialize camera...");
  }
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while(WiFi.status() != WL_CONNECTED ) {
    delay(1000);
    Serial.println("Connecting to WiFi....");
  }

  Serial.println("");
  Serial.println("WiFi connected");

  client.setServer(MQTT_BROKER, MQTT_BROKER_PORT);
  client.setBufferSize(100000);
  delay(1000);

  last = millis();
  
}

void loop()
{
  if (!client.connected()) {
    reconnect();
  }else{
    if(millis()-last > 10000){
      fb = esp_camera_fb_get();
      if(fb){
        Serial.print("img size: ");
        Serial.print(fb->len);
        Serial.println(" B");
        client.publish(MQTT_TOPIC, (const uint8_t *)(fb->buf), fb->len);
        Serial.println("image send success");
      }else{
        Serial.println("Camera capture failed");
      }
      last = millis();
    }
  }

  client.loop();
}
