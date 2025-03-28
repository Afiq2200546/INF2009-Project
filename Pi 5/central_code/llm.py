import paho.mqtt.client as mqtt
import json
import os
from ollama import chat
from ollama import ChatResponse
import time
import subprocess
import threading

# MQTT Configuration
BROKER = "192.168.153.1"  # Change this to your MQTT broker
PORT = 1883
TOPIC = "llm"  # Change this to your desired topic

DATA_DIR = "/home/pg14/Desktop/web_interface_2/UserData"
os.makedirs(DATA_DIR, exist_ok=True)

def read_json_file(filename):
    filepath = f"{filename}.json"
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, "r") as json_file:
            try:
                data = json.load(json_file)
                return data.get("data", "")
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON content in {filename}.json")
    return ""

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

    name = read_json_file("name")
    body_temp = read_json_file("bodytemp")
    heart_rate = read_json_file("heartrate")
    age = read_json_file("age")
    temperature = read_json_file("temperature")
    humidity = read_json_file("humidity")
    save_data_to_json(name, age, heart_rate, temperature, humidity, body_temp)
    # detailed_prompt(name, body_temp, heart_rate, age, temperature, humidity, client)

    # Run detailed_prompt in a separate thread
    prompt_thread = threading.Thread(
        target=detailed_prompt, 
        args=(name, body_temp, heart_rate, age, temperature, humidity, client),
        daemon=True  # Ensures the thread exits if the main program stops
    )
    prompt_thread.start()


def detailed_prompt(name, body_temp, heart_rate, age, temperature, humidity, client):
    # Construct the system prompt using CO-STAR framework
    start = time.time()
    
    client.publish("response", "Loading…")
    with open("response.json", "w") as json_file:
        json.dump({"data": "Loading…"}, json_file, indent=4)
    
    system_prompt = (
        "You are a Smart Mirror Health Assistant integrated with a Raspberry Pi and an advanced language model (LLM).\n"
        "Your role is to analyze health-related data from the user, including body temperature, heart rate, age, and other relevant health metrics.\n"
        "You provide insights based on real-time and historical data, helping users understand their health trends and offering personalized wellness recommendations.\n"
        "Context: Process and analyze real-time health data (e.g., body temperature, heart rate) while considering the user’s age and trends over time.\n"
        "Objective: Offer health-related insights and practical suggestions to improve the user's well-being.\n"
        "Tone: Supportive, professional, and concise.\n"
        "Style: Clear, informative, and user-friendly.\n"
        "Audience: General users monitoring their health.\n"
        "Input:\n"
        "Name: " + str(name) + "\n"
        "Body Temp: " + str(body_temp) + "\n"
        "Heart Rate: " + str(heart_rate) + " bpm\n"
        "Age: " + str(age) + "\n"
        "Ambient Temperature: " + str(temperature) + "\n"
        "Humidity: " + str(humidity) + "\n"
        "Response:\n"
        "Provide accurate, evidence-based interpretations of health data.\n"
        "Suggest simple, actionable health improvements (e.g., 'Your heart rate is slightly elevated. Try deep breathing exercises or hydration.').\n"
        "If necessary, encourage the user to seek medical advice for concerning trends.\n"
        "Politely decline questions unrelated to health and wellness.\n"
        "Summarise and limit to 3 sentences for your response.\n"
    )

    print("Input:")
    print(system_prompt)

    response: ChatResponse = chat(model='qwen2.5:3b', messages=[
        {
            'role': 'user',
            'content': system_prompt,
        },
    ])
    print(response['message']['content'])

    output_llm = response['message']['content']

    command = f'echo "{output_llm}" | ./piper --model en_US-amy-low.onnx --output-raw | aplay -r 16000 -f S16_LE -t raw -'

    client.publish("response", response['message']['content'])
    subprocess.run(command, shell=True, check=True)
    with open("response.json", "w") as json_file:
        json.dump({"data": response['message']['content']}, json_file, indent=4)

    # client.publish("tts_response", response['message']['content'], retain=True)
    with open("tts_response.json", "w") as json_file:
        json.dump({"data": response['message']['content']}, json_file, indent=4)
    
    time.sleep(15)
    client.publish("response", '')
    
    end = time.time()
    length = end - start
    print("\nIt took", length, "seconds!")

def save_data_to_json(name, age, heartrate, temperature, humidity, bodytemp):
    filename = os.path.join(DATA_DIR, f"{name}.json")
    record = {
        "heartrate": heartrate,
        "temperature": temperature,
        "humidity": humidity,
        "bodytemp": bodytemp,
        "time_recorded": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
        data["records"].append(record)
    else:
        data = {
            "username": name,
            "age": age,
            "records": [record]
        }
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()
