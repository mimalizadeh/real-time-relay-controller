idf_component_register(
    SRCS "src/main.c" "src/app_tasks.c" "src/sntp_manager.c" "src/mqtt_manager.c" "src/wifi_manager.c"
    INCLUDE_DIRS "."
    REQUIRES driver esp_driver_gpio esp_wifi nvs_flash esp_event mqtt freertos lwip esp_system esp_netif
)