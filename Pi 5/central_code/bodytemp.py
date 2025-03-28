import paho.mqtt.client as mqtt
import json
import os

# MQTT Configuration
BROKER = "192.168.153.1"  # Change this to your MQTT broker
PORT = 1883
TOPIC = "bodytemp"  # Change this to your desired topic

def on_connect(client, userdata, flags, reasonCode, properties):
    if reasonCode == 0:
        print(f"Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {reasonCode}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    topic_filename = f"{msg.topic.replace('/', '_')}.json"  # Convert topic to filename
    
    try:
        # Attempt to parse JSON, if applicable
        data = json.loads(payload)
    except json.JSONDecodeError:
        # If not JSON, treat it as plain text or number
        if payload.replace('.', '', 1).isdigit():
            data = float(payload) if '.' in payload else int(payload)
        else:
            data = payload
    
    # Write or update the JSON file
    with open(topic_filename, "w") as json_file:
        json.dump({"data": data}, json_file, indent=4)
        
    print(f"Updated {topic_filename} with new data: " + str(data))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()
