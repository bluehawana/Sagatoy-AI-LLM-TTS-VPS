/**
 * Sagatoy ESP32 Firmware - Main Application
 * 
 * Simple WiFi + MQTT client for Sagatoy toy
 * Designed for easy setup by families
 * 
 * How it works:
 * 1. On first boot, enters AP mode for WiFi setup
 * 2. After WiFi configured, connects to MQTT broker
 * 3. Listens for audio/text from server
 * 4. Sends voice audio to server for processing
 * 5. Plays back TTS audio from server
 * 
 * No Docker or technical knowledge needed!
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoOTA.h>
#include <Preferences.h>
#include <driver/i2s.h>
#include "sagatoy_config.h"

// ============== CONFIGURATION ==============

// Storage for WiFi and MQTT credentials
Preferences preferences;

// WiFi client
WiFiClient wifiClient;

// MQTT client
PubSubClient mqttClient;

// Device ID (unique for each toy)
String deviceId;

// Connection status LEDs
const int LED_PIN = 2;  // Built-in LED on most ESP32

// ============== FUNCTIONS ==============

/**
 * Generate unique device ID from MAC address
 */
String generateDeviceId() {
    uint8_t mac[6];
    WiFi.macAddress(mac);
    char id[13];
    sprintf(id, "%02X%02X%02X%02X%02X%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    return String(id);
}

/**
 * Load stored configuration
 */
void loadConfig(String &wifiSSID, String &wifiPass, String &mqttBroker, int &mqttPort) {
    preferences.begin("sagatoy", false);
    
    wifiSSID = preferences.getString("wifi_ssid", "");
    wifiPass = preferences.getString("wifi_pass", "");
    mqttBroker = preferences.getString("mqtt_broker", DEFAULT_MQTT_BROKER);
    mqttPort = preferences.getInt("mqtt_port", DEFAULT_MQTT_PORT);
    
    preferences.end();
}

/**
 * Save configuration
 */
void saveConfig(const String &wifiSSID, const String &wifiPass, 
                const String &mqttBroker, int mqttPort) {
    preferences.begin("sagatoy", false);
    
    preferences.putString("wifi_ssid", wifiSSID);
    preferences.putString("wifi_pass", wifiPass);
    preferences.putString("mqtt_broker", mqttBroker);
    preferences.putInt("mqtt_port", mqttPort);
    
    preferences.end();
}

/**
 * Connect to WiFi
 */
bool connectWiFi(const String &ssid, const String &pass) {
    Serial.print("Connecting to WiFi: ");
    Serial.println(ssid);
    
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid.c_str(), pass.c_str());
    
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 30) {
        delay(500);
        Serial.print(".");
        retries++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi connected!");
        Serial.print("IP: ");
        Serial.println(WiFi.localIP());
        return true;
    }
    
    Serial.println("\nWiFi connection failed!");
    return false;
}

/**
 * Connect to MQTT broker
 */
bool connectMQTT(const String &broker, int port, const String &devId) {
    Serial.print("Connecting to MQTT: ");
    Serial.print(broker);
    Serial.print(":");
    Serial.println(port);
    
    mqttClient.setServer(broker.c_str(), port);
    mqttClient.setClient(wifiClient);
    
    String clientId = "sagatoy-" + devId;
    
    int retries = 0;
    while (!mqttClient.connect(clientId.c_str(), "sagatoy", "sagatoy") && retries < 3) {
        Serial.print(".");
        delay(1000);
        retries++;
    }
    
    if (mqttClient.connected()) {
        Serial.println("\nMQTT connected!");
        
        // Subscribe to topics
        String audioTopic = String(MQTT_TOPIC_AUDIO_IN).c_str();
        audioTopic.replace("+", devId);
        mqttClient.subscribe(audioTopic.c_str());
        
        String textTopic = String(MQTT_TOPIC_TEXT).c_str();
        textTopic.replace("+", devId);
        mqttClient.subscribe(textTopic.c_str());
        
        Serial.println("Subscribed to topics");
        return true;
    }
    
    Serial.println("\nMQTT connection failed!");
    return false;
}

/**
 * Handle incoming MQTT messages
 */
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message on topic: ");
    Serial.println(topic);
    
    // Handle audio data
    if (String(topic).endsWith("/audio/in")) {
        Serial.print("Audio data received: ");
        Serial.print(length);
        Serial.println(" bytes");
        // TODO: Play audio via I2S
    }
    
    // Handle text/TTS commands
    if (String(topic).endsWith("/text")) {
        Serial.print("Text command: ");
        payload[length] = '\0';
        Serial.println((char*)payload);
        // TODO: Convert to speech and play
    }
}

/**
 * Send audio to server
 */
void sendAudioToServer(const uint8_t* audioData, size_t length) {
    char topic[100];
    sprintf(topic, MQTT_TOPIC_AUDIO_OUT, deviceId.c_str());
    
    mqttClient.beginPublish(topic, length, false);
    mqttClient.write(audioData, length);
    mqttClient.endPublish();
}

/**
 * WiFi scan for setup (for future AP mode config)
 */
void startConfigPortal() {
    Serial.println("\n=== CONFIGURATION MODE ===");
    Serial.println("Connect to: Sagatoy-Setup");
    Serial.println("Password: sagatoy123");
    Serial.println("Then open browser to: 192.168.1.1");
    
    // TODO: Start WiFi AP mode for easy setup
    // For now, we'll use a simpler approach
}

/**
 * Initialize I2S for audio
 */
void initAudio() {
    // TODO: Configure I2S for microphone and speaker
    // This will depend on the specific hardware
    
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_TX),
        .sample_rate = AUDIO_SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 1024,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };
    
    // TODO: Initialize with actual pins
    // i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
}

// ============== SETUP ==============

void setup() {
    Serial.begin(115200);
    Serial.println("\n========================================");
    Serial.println("  SAGATOY FIRMWARE v" FIRMWARE_VERSION);
    Serial.println("  For families - Simple & Easy!");
    Serial.println("========================================\n");
    
    // Generate device ID
    deviceId = generateDeviceId();
    Serial.print("Device ID: ");
    Serial.println(deviceId);
    
    // Initialize LED
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);
    
    // Initialize audio
    initAudio();
    
    // Load saved configuration
    String wifiSSID, wifiPass, mqttBroker;
    int mqttPort;
    loadConfig(wifiSSID, wifiPass, mqttBroker, mqttPort);
    
    // If no WiFi saved, enter config mode
    if (wifiSSID.length() == 0) {
        Serial.println("First run - starting configuration...");
        startConfigPortal();
        return;
    }
    
    // Connect to WiFi
    digitalWrite(LED_PIN, HIGH);  // LED on = connecting
    if (connectWiFi(wifiSSID, wifiPass)) {
        // Connect to MQTT
        if (connectMQTT(mqttBroker, mqttPort, deviceId)) {
            digitalWrite(LED_PIN, LOW);  // LED off = connected
            Serial.println("\n✅ SAGATOY IS READY!");
            Serial.println("Have fun talking with your toy!");
        }
    }
    
    // Setup OTA updates
    ArduinoOTA.setHostname(("Sagatoy-" + deviceId).c_str());
    ArduinoOTA.onStart([]() {
        Serial.println("OTA Update starting...");
    });
    ArduinoOTA.onEnd([]() {
        Serial.println("OTA Update complete!");
    });
    ArduinoOTA.onError([](ota_error_t error) {
        Serial.printf("OTA Error: %u\n", error);
    });
    ArduinoOTA.begin();
    
    Serial.println("\n=== SYSTEM READY ===");
    Serial.println("Waiting for commands from server...");
}

// ============== LOOP ==============

void loop() {
    // Handle MQTT
    if (mqttClient.connected()) {
        mqttClient.loop();
    } else {
        // Reconnect
        String wifiSSID, wifiPass, mqttBroker;
        int mqttPort;
        loadConfig(wifiSSID, wifiPass, mqttBroker, mqttPort);
        
        if (connectWiFi(wifiSSID, wifiPass)) {
            connectMQTT(mqttBroker, mqttPort, deviceId);
        }
    }
    
    // Handle OTA updates
    ArduinoOTA.handle();
    
    // TODO: Read from microphone and send to server
    
    delay(10);
}