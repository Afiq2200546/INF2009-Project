# This is the code to run the MLX90614 Infrared Thermal Sensor
# You'll need to import the package "Adafruit Blinka"
# You'll need to import the package "adafruit-circuitpython-mlx90614/"
# You'll need to enable i2c on the pi https://pimylifeup.com/raspberry-pi-i2c/
# Reboot after enabling i2C
# Sensor is connected to 3.3V, GND and the i2C pins 3(SDA) and 5(SCL)

import board
import busio as io
import adafruit_mlx90614

from time import sleep
import paho.mqtt.client as mqtt

i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Connect to the broker
client.connect("0.0.0.0", 1883)

while True:
    try:
        ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
        targetTemp = "{:.2f}".format(mlx.object_temperature)

        client.publish("bodytemp", targetTemp)
        sleep(1)

        print("Ambient Temperature:", ambientTemp, "°C")
        print("Target Temperature:", targetTemp,"°C")
    except RuntimeError as err:
        print(err.args[0])

    sleep(2.0)

client.disconnect()