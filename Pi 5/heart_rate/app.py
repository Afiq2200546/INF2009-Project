import radar_sensor 
import time
import paho.mqtt.client as mqtt
# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Connect to the broker
client.connect("192.168.153.1", 1883)

while True:
    try:
        heartrate = str(radar_sensor.get_heart_rate())
        client.publish("heartrate", heartrate)
        print(heartrate)
    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)

client.disconnect()