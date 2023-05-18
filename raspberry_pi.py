import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime
import sqlite3

# MQTT Configuration
broker_address = "mqtt.example.com"
broker_port = 1883
topic_sensor_data = "greenhouse/sensor"
topic_control_commands = "greenhouse/control"

# Database Configuration
database_name = "greenhouse.db"

# Sensor and Actuator Pin Configurations
# GPIO pin numbers or addresses
temperature_sensor_pin = 1
humidity_sensor_pin = 2
light_sensor_pin = 3
soil_moisture_sensor_pin = 4
fan_pin = 5
heater_pin = 6
irrigation_pin = 7

# Connect to MQTT Broker
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(topic_control_commands)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Received message: " + message)
    # Parse control commands and adjust actuators accordingly

def read_sensor(sensor_pin):
    # Read sensor data from the specified pin
    # Replace with actual sensor reading implementation
    return random.uniform(0, 100)  # Placeholder random values

def control_actuator(actuator_pin, value):
    # Control the specified actuator pin with the given value
    # Replace with actual actuator control implementation
    print("Controlling actuator", actuator_pin, "with value", value)

def log_data(sensor_data):
    # Log sensor data into the database
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (timestamp, temperature, humidity, light, moisture) VALUES (?, ?, ?, ?, ?)",
              (timestamp, sensor_data["temperature"], sensor_data["humidity"], sensor_data["light"], sensor_data["moisture"]))
    conn.commit()
    conn.close()

def main_loop():
    while True:
        # Read sensor data
        temperature = read_sensor(temperature_sensor_pin)
        humidity = read_sensor(humidity_sensor_pin)
        light = read_sensor(light_sensor_pin)
        moisture = read_sensor(soil_moisture_sensor_pin)
        
        # Create sensor data dictionary
        sensor_data = {
            "temperature": temperature,
            "humidity": humidity,
            "light": light,
            "moisture": moisture
        }
        
        # Publish sensor data to MQTT broker
        client.publish(topic_sensor_data, str(sensor_data))
        
        # Log sensor data into the database
        log_data(sensor_data)
        
        # Wait for a few seconds before the next iteration
        time.sleep(5)

# Connect MQTT client
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)

# Initialize the database
conn = sqlite3.connect(database_name)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (timestamp TEXT, temperature REAL, humidity REAL, light REAL, moisture REAL)''')
conn.commit()
conn.close()

# Start the main loop
main_loop()
