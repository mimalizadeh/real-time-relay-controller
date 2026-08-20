#include "include/sntp_manager.h"
#include "esp_sntp.h"
#include "esp_log.h"
#include "freertos/task.h"

static const char *TAG = "SNTP_MGR";

void initialize_sntp(void) {
    ESP_LOGI(TAG, "Initializing SNTP...");
    esp_sntp_setoperatingmode(SNTP_OPMODE_POLL);
    esp_sntp_setservername(0, "pool.ntp.org");
    esp_sntp_init();

    int retry = 0;
    const int retry_count = 15;
    while (sntp_get_sync_status() == SNTP_SYNC_STATUS_RESET && ++retry < retry_count) {
        ESP_LOGI(TAG, "Waiting for system time to be set... (%d/%d)", retry, retry_count);
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
    
    if (retry == retry_count) {
        ESP_LOGE(TAG, "Failed to synchronize time via NTP. Timestamps will be invalid.");
    } else {
        ESP_LOGI(TAG, "Time synchronized successfully.");
    }
}