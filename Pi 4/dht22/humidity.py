import time
import adafruit_dht
import board
import paho.mqtt.client as mqtt

dht_device = adafruit_dht.DHT22(board.D4)
# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Connect to the broker
client.connect("0.0.0.0", 1883)

while True:
    try:
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        humidity = dht_device.humidity

        print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
        client.publish("temperature", "{:.1f} C / {:.1f} F".format(temperature_c, temperature_f))
        client.publish("humidity", "{}%".format(humidity))
    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)

client.loop_forever()