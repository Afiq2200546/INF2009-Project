import paho.mqtt.client as mqtt

# Define the MQTT broker details
MQTT_BROKER = '192.168.153.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'schedule'

# Initialize the MQTT client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Define the callback function for when a message is received
mqtt_payload = None

def on_message(client, userdata, message):
    global mqtt_payload
    mqtt_payload = message.payload.decode()
    print(f"Received message: {mqtt_payload} on topic: {message.topic}")

# Assign the on_message callback function
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

# Subscribe to the topic
mqtt_client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop in a separate thread
mqtt_client.loop_start()
