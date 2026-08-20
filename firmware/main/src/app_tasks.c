#include "include/app_tasks.h"
#include "include/app_config.h"
#include "esp_log.h"
#include <sys/time.h>

#include "driver/gpio.h"

static const char *TAG = "APP_TASKS";

void relay_control_task(void *pvParameters) {
    relay_command_t cmd;
    
    while (1) {
        if (xQueueReceive(command_queue, &cmd, portMAX_DELAY) == pdPASS) {
            ESP_LOGI(TAG, "Executing Command: Relay %d to %s", 
                     cmd.relay_id, cmd.target_state ? "ON" : "OFF");
            
            int gpio_pin = 0;
            switch(cmd.relay_id) {
                case 1: gpio_pin = 19; break;
                case 2: gpio_pin = 21; break;
                case 3: gpio_pin = 22; break;
                case 4: gpio_pin = 23; break;
                default: 
                    ESP_LOGE(TAG, "Invalid Relay ID: %d", cmd.relay_id); 
                    continue;
            }
            
            gpio_config(&(gpio_config_t){
                .pin_bit_mask = (1ULL << gpio_pin),
                .mode = GPIO_MODE_OUTPUT,
                .pull_up_en = GPIO_PULLUP_DISABLE,
                .pull_down_en = GPIO_PULLDOWN_DISABLE,
                .intr_type = GPIO_INTR_DISABLE
            });
            gpio_set_level(gpio_pin, !cmd.target_state);
        }
    }
}