#pragma once

#include <stdint.h>
#include <stdbool.h>

// Octopus board pin definitions
#define PIN_MIC_I2S_BCLK 41
#define PIN_MIC_I2S_LRCK 42
#define PIN_MIC_I2S_DOUT 40

#define PIN_SPK_I2S_BCLK 18
#define PIN_SPK_I2S_LRCK 17
#define PIN_SPK_I2S_DOUT 16

#define PIN_BUTTON_RECORD 5   // Button A
#define PIN_BUTTON_ROLE  6    // Button B
#define PIN_BUTTON_MODE  7    // Button C

#define PIN_LED_DATA     21   // WS2812B LED
#define PIN_RGB_COUNT    1

#define PIN_VOL_POWER    8    // Volume knob / power switch
#define PIN_BATTERY      5    // Battery ADC (GPIO35)
#define PIN_WAKE_UP      9    // Wake sensor

#define APP_WIFI_PROV_STA_SSID     "FoloToy-Config"
#define APP_WIFI_PROV_STA_PASSWD   ""
#define APP_WIFI_PROV_MANUFACTURER "sagatoy"
#define APP_WIFI_PROV_MODEL        "octopus-nordic"
#define APP_WIFI_PROV_ID           "followToy"

// Server configuration
#define DEFAULT_SERVER_IP   "94.72.141.71"
#define DEFAULT_SERVER_PORT 8085
#define DEFAULT_HTTP_PORT   8082
#define DEFAULT_AUDIO_URL   "http://94.72.141.71:8082"
#define DEFAULT_MQTT_HOST   "94.72.141.71"
#define DEFAULT_MQTT_PORT   1883
#define DEFAULT_MQTT_USER   "sagatoy"
#define DEFAULT_MQTT_PASS   "sagatoy"

// Device serial number (use ESP32 MAC as fallback)
#define DEVICE_SN_LEN 32

// Audio configuration
#define AUDIO_SAMPLE_RATE 16000
#define AUDIO_CHUNK_SIZE 640    // 40ms at 16kHz, 16-bit mono
#define AUDIO_I2S_CHANNELS 1
#define AUDIO_I2S_BITS_PER_SAMPLE 16

// Button timeout
#define BUTTON_HOLD_MS 500

// WiFi provisioning mode
#define AP_MODE_TIMEOUT_S 300

// Maximum TTS audio size (256KB)
#define MAX_TTS_AUDIO_SIZE (256 * 1024)
#define TTS_DOWNLOAD_TIMEOUT_S 10

// Buffer for TTS audio
#define TTS_RECV_BUF_SIZE (4 * 1024)
