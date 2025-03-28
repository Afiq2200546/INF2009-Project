#!/usr/bin/env python3

import argparse
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json  # Needed to parse Vosk output

import paho.mqtt.client as mqtt
import time
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("192.168.153.1", 1883)

client.loop_start()

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def detect_keywords(text):
    """Detects keywords in the recognized text and triggers actions."""
    if any(kw in text for kw in ["temperature", "body temperature", "check temperature"]):
        print("✅ Trigger: BODY TEMPERATURE")
        # TODO: Call your temperature module here

    elif any(kw in text for kw in ["heart rate", "heartbeat", "pulse"]):
        print("✅ Trigger: HEART RATE")
        # TODO: Call your heart rate module here

    elif any(kw in text for kw in ["alarm", "set alarm", "wake me up"]):
        print("✅ Trigger: ALARM")
        # TODO: Call your alarm module here

    elif any(kw in text for kw in ["health analysis", "healthanalysis", "analyze", "analysis"]):
        print("✅ Trigger: health analysis")
        # TODO: Call your llm module here
        client.publish("llm", 'start')
        print("client.publish('llm', 'start')")
        time.sleep(1)  # Allow time for the message to be sent
        

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-l", "--list-devices", action="store_true",
                    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument("-f", "--filename", type=str, metavar="FILENAME",
                    help="audio file to store recording to")
parser.add_argument("-d", "--device", type=int_or_str,
                    help="input device (numeric ID or substring)")
parser.add_argument("-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument("-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])
        
    model = Model(lang=args.model if args.model else "en-us")

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize=2048, device=args.device,
                           dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())  # Convert Vosk JSON output to a dictionary
                text = result.get("text", "").lower()  # Extract text and convert to lowercase
                print(f"Recognized: {text}")
                detect_keywords(text)  # Call the keyword detection function
            else:
                print(rec.PartialResult())

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    # client.disconnect()
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))

