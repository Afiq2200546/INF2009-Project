import paho.mqtt.client as mqtt
import json
import os
import time

# MQTT Configuration
BROKER = "192.168.153.1"  # Change this to your MQTT broker
PORT = 1883
TOPIC = "tts_response"  # Change this to your desired topic

# Construct the filename from the topic
topic_filename = f"{TOPIC.replace('/', '_')}.json"

def publish_json():
    if os.path.exists(topic_filename) and os.path.getsize(topic_filename) > 0:
        with open(topic_filename, "r") as json_file:
            try:
                data = json.load(json_file)
                if not data:  # Check if JSON content is empty
                    print("JSON file is empty. No data to publish.")
                    return
            except json.JSONDecodeError:
                print("Error: Invalid JSON file content.")
                return
        
        # Publish the JSON content
        client.publish(TOPIC, json.dumps(data["data"]))
        print(f"Published data: {data['data']}")
        
        # Clear the file
        with open(topic_filename, "w") as json_file:
            json.dump({}, json_file)
            print(f"Cleared {topic_filename}")
    else:
        print(f"File {topic_filename} does not exist or is empty.")

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# # while True:
# #     publish_json()
# publish_json()
# # client.loop_forever()
# client.loop_start()

while True:
    publish_json()
    time.sleep(5)  # Adjust the interval as needed

client.loop_start()
