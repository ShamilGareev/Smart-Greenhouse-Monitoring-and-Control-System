import paho.mqtt.client as mqtt

# MQTT Configuration
broker_address = "mqtt.example.com"
broker_port = 1883
topic_sensor_data = "greenhouse/sensor"

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(topic_sensor_data)
    else:
        print("Failed to connect to MQTT Broker")

# Callback function for incoming MQTT messages
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    # Process the incoming sensor data message
    process_sensor_data(message)

# Function to process sensor data
def process_sensor_data(data):
#
#
    print("Received Sensor Data:", data)

# Connect to MQTT Broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)

# Start the MQTT client loop
client.loop_forever()

    
    # Example: Display the sensor data
    print("Received Sensor Data:", data)

# Connect to MQTT Broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)

# Start the MQTT client loop
client.loop_forever()
