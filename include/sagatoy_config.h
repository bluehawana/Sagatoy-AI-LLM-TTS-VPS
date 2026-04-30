/**
 * Sagatoy ESP32 Firmware - Simple MQTT Client
 * 
 * For families: Just power on and it works!
 * No configuration needed - connects to Sagatoy cloud by default.
 * 
 * Features:
 * - Auto-connect to WiFi (stored credentials)
 * - Auto-connect to MQTT broker (Sagatoy server)
 * - Audio streaming via MQTT
 * - Over-the-air (OTA) updates support
 * 
 * Hardware: ESP32-WROOM-32 (or compatible)
 * 
 * Author: Sagatoy Team
 * License: MIT
 */

#ifndef SAGATOY_CONFIG_H
#define SAGATOY_CONFIG_H

// ===== SAGATOY SERVER CONFIGURATION =====
// Default Sagatoy Cloud servers (can be changed via config)
#define DEFAULT_MQTT_BROKER "mqtt.sagatoy.ai"
#define DEFAULT_MQTT_PORT 1883
#define DEFAULT_API_SERVER "https://api.sagatoy.ai"

// ===== DEVICE CONFIGURATION =====
#define DEVICE_NAME "Sagatoy-Toy"
#define DEVICE_TYPE "octopus"
#define FIRMWARE_VERSION "1.0.0"

// ===== MQTT TOPICS =====
// Subscribe to these topics
#define MQTT_TOPIC_AUDIO_IN "sagatoy/+/audio/in"
#define MQTT_TOPIC_TEXT "sagatoy/+/text"
#define MQTT_TOPIC_CONFIG "sagatoy/+/config"

// Publish to these topics  
#define MQTT_TOPIC_AUDIO_OUT "sagatoy/%s/audio/out"
#define MQTT_TOPIC_STATUS "sagatoy/%s/status"
#define MQTT_TOPIC_EVENT "sagatoy/%s/event"

// ===== WiFi CONFIGURATION =====
#define WIFI_CONNECT_TIMEOUT_MS 15000
#define WIFI_MAX_RETRY 5

// ===== MQTT CONFIGURATION =====
#define MQTT_CONNECT_TIMEOUT_MS 10000
#define MQTT_KEEPALIVE_SEC 60
#define MQTT_MAX_RETRY 3

// ===== AUDIO CONFIGURATION =====
#define AUDIO_BUFFER_SIZE 4096
#define AUDIO_SAMPLE_RATE 16000
#define AUDIO_CHANNELS 1

// ===== LED INDICATORS =====
#define LED_WIFI_CONNECTING 0x0000FF  // Blue - connecting to WiFi
#define LED_MQTT_CONNECTING 0x00FF00  // Green - connecting to MQTT
#define LED_READY 0xFF0000            // Red - ready (working)
#define LED_ERROR 0xFF00FF            // Purple - error

#endif // SAGATOY_CONFIG_H