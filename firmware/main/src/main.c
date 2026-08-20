#include "esp_log.h"
#include "include/app_config.h"
#include "include/app_tasks.h"
#include "include/mqtt_manager.h"
#include "include/sntp_manager.h"
#include "include/wifi_manager.h"
#include "nvs_flash.h"

static const char *TAG = "APP_MAIN";

EventGroupHandle_t s_app_event_group;
QueueHandle_t command_queue;

void app_main(void) {
  esp_err_t ret = nvs_flash_init();
  if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
      ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
    ESP_ERROR_CHECK(nvs_flash_erase());
    ret = nvs_flash_init();
  }
  ESP_ERROR_CHECK(ret);

  // 1. Initialize Inter-Task Communication FIRST
  command_queue = xQueueCreate(COMMAND_QUEUE_SIZE, sizeof(relay_command_t));
  if (command_queue == NULL) {
    ESP_LOGE(TAG, "Failed to allocate command queue. Halting.");
    return;
  }

  // 2. Network Bring-up
  wifi_init_sta();
  
  // 3. NTP Sync (Required for trading timestamps)
  initialize_sntp();

  // 4. MQTT Bring-up
  mqtt_app_start();

  // 5. Start Application Tasks
  xTaskCreate(relay_control_task, "MQTT_Pub", 4096, NULL, 5, NULL);
}