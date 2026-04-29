/**
 * FoloToy Nordic - ESP32-S3 Firmware for Octopus Board
 * 
 * Pushes I2S microphone audio to server via UDP (port 8085),
 * downloads TTS audio from HTTP server (port 8082),
 * reports events via MQTT.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "freertos/queue.h"

#include "esp_log.h"
#include "esp_event.h"
#include "esp_wifi.h"
#include "esp_sleep.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_netif.h"

// WiFi Provisioning
#include "wifi_provisioning/manager.h"
#include "wifi_provisioning/scheme_softap.h"

// Components
#include "app_config.h"
#include "fw_main.h"
#include "led_control.h"
#include "button_input.h"
#include "i2s_audio.h"
#include "udp_client.h"
#include "http_client.h"
#include "mqtt_manager.h"
#include "config_store.h"

static const char *TAG = "folotoy";

static device_state_t g_state = STATE_STANDBY;
static EventGroupHandle_t s_event_group;

#define STATE_AP_BIT         BIT0
#define STATE_WIFI_BIT       BIT1
#define STATE_SERVER_BIT     BIT2

device_state_t fw_get_state(void)
{
    return g_state;
}

// State management
static void set_state(device_state_t new_state)
{
    g_state = new_state;

    switch (new_state) {
    case STATE_STANDBY:
        led_set_color(0x00, 0x00, 0x00);
        break;
    case STATE_AP_CONFIG:
        led_breathe(0, 0, 255); // Blue breathing
        break;
    case STATE_WIFI_CONNECTING:
        led_breathe(0, 165, 255); // Light blue breathing
        break;
    case STATE_CONNECTED:
        led_set_color(0, 255, 0); // Solid green
        break;
    case STATE_RECORDING:
        led_set_color(0, 255, 0, ); // Solid green
        break;
    case STATE_SENDING_AUDIO:
        led_breathe(0, 255, 0); // Green breathing
        break;
    case STATE_PROCESSING:
        led_breathe(0, 255, 0); // Green breathing
        break;
    case STATE_DOWNLOADING_TTS:
        led_breathe(0, 165, 255); // Light blue
        break;
    case STATE_PLAYING_AUDIO:
        led_breathe(0, 255, 0); // Green breathing
        break;
    case STATE_ERROR:
        led_set_color(255, 0, 0); // Solid red
        break;
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "FoloToy Nordic v1.0.0 starting...");
    ESP_LOGI(TAG, "Chip: %s, Rev: %d", esp_get_chip_model_name(), esp_get_chip_revision());

    // Initialize non-volatile storage
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_LOGI(TAG, "Erase NVS partition");
        nvs_flash_erase();
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Load configuration
    config_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    config_load(&cfg);

    // Initialize WiFi and network
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    // Create default WiFi station interface
    esp_netif_t *sta_netif = esp_netif_new(&esp_netif_default_config_for_wifi_sta);

    // Create default WiFi AP interface for provisioning
    esp_netif_t *ap_netif = esp_netif_new(&esp_netif_default_config_for_wifi_ap);

    wifi_init_config_t cfg_wifi = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg_wifi));

    // Configure Wi-Fi provisioning
    wifi_provisioning_config_t prov_cfg = {
        .scheme = wifi_provisioning_scheme_softap,
        .scheme_opt = PROV_TASK_OPT_MDNS_ENABLED,
        .scheme_opt_mask = PROV_TASK_OPT_MDNS_ENABLED,
    };

    ESP_ERROR_CHECK(wifi_provisioning_init(&prov_cfg));

    // Register provisioning with ESP-IDF
    ESP_ERROR_CHECK(esp_event_handler_register(PROVISIONING_MANUAL_STATE_ENTER_EVENT,
                                               PROVISIONING_ST_MANUAL_START,
                                               wifi_provisioning_set_manual_start_event_handler,
                                               NULL));

    // Start provisioning if not configured
    bool configured;
    config_is_wifi_configured(&configured);
    if (!configured) {
        ESP_LOGI(TAG, "No WiFi config, starting AP provisioning");
        set_state(STATE_AP_CONFIG);
    }

    // Start network provisioning task
    wifi_provisioning_start();

    // Initialize all components
    fw_init(&cfg);

    // Main loop
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));

        switch (g_state) {
        case STATE_AP_CONFIG:
            // Wi-Fi provisioning handles AP automatically
            break;
        case STATE_CONNECTED:
            // Already initialized, do nothing
            break;
        case STATE_ERROR:
            ESP_LOGE(TAG, "Resetting after error...");
            vTaskDelay(pdMS_TO_TICKS(5000));
            esp_restart();
            break;
        default:
            break;
        }
    }
}
