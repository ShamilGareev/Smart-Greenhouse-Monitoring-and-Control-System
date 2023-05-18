#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <mqtt.h>

#define BROKER_ADDRESS "mqtt.example.com"
#define BROKER_PORT 1883
#define TOPIC_SENSOR_DATA "greenhouse/sensor"

// MQTT client structure
mqtt_client_t client;

// Callback function for MQTT connection
void on_connect(mqtt_client_t* client, int result) {
    if (result == MQTT_CONNECT_SUCCESS) {
        printf("Connected to MQTT Broker\n");
    } else {
        printf("Failed to connect to MQTT Broker\n");
    }
}

// Function to generate random measurements
float generate_measurement() {
    return (float)rand() / RAND_MAX * 100.0;
}

// Function to publish sensor data to MQTT broker
void publish_sensor_data(mqtt_client_t* client) {
    // Generate random measurements
    float temperature = generate_measurement();
    float humidity = generate_measurement();
    float light = generate_measurement();
    float moisture = generate_measurement();

    // Create JSON payload
    char payload[256];
    snprintf(payload, sizeof(payload), "{\"temperature\": %.2f, \"humidity\": %.2f, \"light\": %.2f, \"moisture\": %.2f}",
        temperature, humidity, light, moisture);

    // Publish the sensor data to the MQTT broker
    mqtt_publish(client, TOPIC_SENSOR_DATA, payload, strlen(payload), MQTT_PUBLISH_QOS_0);
    printf("Published Sensor Data: %s\n", payload);
}

int main() {
    // Initialize MQTT client
    mqtt_init(&client);

    // Set MQTT broker address and port
    mqtt_set_broker(&client, BROKER_ADDRESS, BROKER_PORT);

    // Set MQTT connection callback
    mqtt_set_connect_callback(&client, on_connect);

    // Connect to MQTT broker
    mqtt_connect(&client);

    // Seed the random number generator
    srand(time(NULL));

    // Main loop
    while (1) {
        // Publish sensor data every 5 seconds
        publish_sensor_data(&client);
        mqtt_yield(&client, 5000);
    }

    // Disconnect from MQTT broker
    mqtt_disconnect(&client);

    return 0;
}
