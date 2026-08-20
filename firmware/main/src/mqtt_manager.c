#include "include/mqtt_manager.h"
#include "include/app_config.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "MQTT_MGR";
esp_mqtt_client_handle_t mqtt_client = NULL;

static void mqtt_event_handler(void *handler_args, esp_event_base_t base,
                               int32_t event_id, void *event_data) {
  esp_mqtt_event_handle_t event = event_data;

  const char *subscribe_topic = "devices/node1/commands/relay/+/set";
  
  const char *sscanf_format = "devices/node1/commands/relay/%d/set";

  switch ((esp_mqtt_event_id_t)event_id) {
  case MQTT_EVENT_CONNECTED:
    ESP_LOGI(TAG, "MQTT Connected to Broker");
    xEventGroupSetBits(s_app_event_group, MQTT_CONNECTED_BIT);
    
    int msg_id = esp_mqtt_client_subscribe(mqtt_client, subscribe_topic, 1);
    ESP_LOGI(TAG, "Subscribed to commands, msg_id=%d", msg_id);
    break;
    
  case MQTT_EVENT_DISCONNECTED:
    ESP_LOGW(TAG, "MQTT Disconnected from Broker");
    xEventGroupClearBits(s_app_event_group, MQTT_CONNECTED_BIT);
    break;
    
  case MQTT_EVENT_ERROR:
    if (event->error_handle->error_type == MQTT_ERROR_TYPE_TCP_TRANSPORT) {
      ESP_LOGE(TAG, "MQTT TCP Transport Error: %s",
               strerror(event->error_handle->esp_transport_sock_errno));
    }
    break;
    
  case MQTT_EVENT_DATA:
    ESP_LOGI(TAG, "MQTT_EVENT_DATA Received on topic: %.*s", event->topic_len, event->topic);
    
    relay_command_t command;
    char topic_str[64];
    
    snprintf(topic_str, sizeof(topic_str), "%.*s", event->topic_len, event->topic);
    
    if (sscanf(topic_str, sscanf_format, &command.relay_id) == 1) {
        
        if (strnstr(event->data, "ON", event->data_len) != NULL) {
          command.target_state = 1;
        } else {
          command.target_state = 0;
        }

        if (xQueueSend(command_queue, &command, 0) == pdPASS) {
          ESP_LOGI(TAG, "Command queued for Relay %d -> State: %d",
                   command.relay_id, command.target_state);
        } else {
          ESP_LOGE(TAG, "Command queue is FULL! Dropping command.");
        }
    } else {
        ESP_LOGW(TAG, "Failed to parse relay ID from topic: %s", topic_str);
    }
    break;

  default:
    break;
  }
}

void mqtt_app_start(void) {
  esp_mqtt_client_config_t mqtt_cfg = {
      .broker.address.uri = MQTT_BROKER_URI,
      .network.disable_auto_reconnect = false, // Explicitly enable
  };
  mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
  esp_mqtt_client_register_event(mqtt_client, ESP_EVENT_ANY_ID,
                                 mqtt_event_handler, NULL);
  esp_mqtt_client_start(mqtt_client);
}