#pragma once

#include "esp_err.h"

typedef enum {
    STATE_STANDBY,
    STATE_AP_CONFIG,
    STATE_WIFI_CONNECTING,
    STATE_CONNECTED,
    STATE_RECORDING,
    STATE_SENDING_AUDIO,
    STATE_PROCESSING,
    STATE_DOWNLOADING_TTS,
    STATE_PLAYING_AUDIO,
    STATE_ERROR,
} device_state_t;

typedef enum {
    ROLE_STANDBY,
    ROLE_RECORD,
    ROLE_PROCESS,
    ROLE_PLAYBACK
} role_t;

// Persistent configuration stored in NVS
typedef struct {
    char server_host[64];
    int server_port;
    char http_url[128];
    char mqtt_host[64];
    int mqtt_port;
    char mqtt_user[32];
    char mqtt_pass[32];
    char sn[DEVICE_SN_LEN];
    bool wifi_configured;
    uint8_t wifi_rssi;
    char sta_ssid[32];
    char sta_pass[32];
} config_t;

esp_err_t fw_init(config_t *cfg);
device_state_t fw_get_state(void);
