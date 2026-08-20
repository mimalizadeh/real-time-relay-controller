#ifndef APP_CONFIG_H
#define APP_CONFIG_H

#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/queue.h"

/* Network Configuration */
#define ESP_WIFI_SSID       CONFIG_WIFI_SSID
#define ESP_WIFI_PASS       CONFIG_WIFI_PASSWORD
#define MQTT_BROKER_URI     CONFIG_MQTT_BROKER_URI
#define ESP_MAXIMUM_RETRY   5
#define SIGNAL_QUEUE_SIZE   20

#define COMMAND_QUEUE_SIZE   20

/* Event Group Bits */
#define WIFI_CONNECTED_BIT  BIT0
#define WIFI_FAIL_BIT       BIT1
#define MQTT_CONNECTED_BIT  BIT2

/* Global Variables (Extern) */
extern EventGroupHandle_t s_app_event_group;

extern QueueHandle_t command_queue;

typedef struct {
    int relay_id;     
    int target_state; 
} relay_command_t;

#endif // APP_CONFIG_H