import serial
import struct
import time
import threading

# Serial connection
ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1)

latest_data = {
    "Heart Rate": None,
    "Breathing Value": None,
    "Breathing Rate": None,
    "Breathing Status": None,
    "Body Movement Intensity": None,
    "Distance": None
}


def compute_checksum(packet):
    """Calculate checksum."""
    return sum(packet[:-3]) & 0xFF  # Excluding last 3 bytes (checksum and end)


def compute_checksum(packet):
    """Calculate checksum."""
    return sum(packet[:-3]) & 0xFF  # Excluding last 3 bytes (checksum and end)


def parse_data(packet):
    """Parses a sensor data packet and updates the latest readings."""
    if not (packet.startswith(b'\x53\x59') and packet.endswith(b'\x54\x43')):
        return

    control_word = packet[2]
    command_word = packet[3]
    length = struct.unpack("<H", packet[4:6])[0]
    payload = packet[6:-3]

    if compute_checksum(packet) != packet[-3]:
        return

    # Presence Detection
    if control_word == 0x80:
        if command_word == 0x03:
            latest_data["Body Movement Intensity"] = payload[0]
        elif command_word == 0x04:
            latest_data["Distance"] = struct.unpack(">H", payload[:2])[0]
   
    # Respiratory Rate
    elif control_word == 0x81:
        if command_word == 0x01:
            # Breathing Information
            if payload[0] in [0x01, 0x02, 0x03, 0x04]:
                breathing_status = {0x01: "Normal", 0x02: "Fast Breathing", 
                                    0x03: "Slow Breathing", 0x04: "None"}
                latest_data["Breathing Status"] = breathing_status[payload[0]]
                #print(f"Breathing Status: {breathing_status[payload[0]]}")

            # Breathing Values
            elif 0 <= payload[0] <= 25:
                latest_data["Breathing Value"] = payload[0]
                #print(f"Breathing Value: {payload[0]} breaths/min")

        # Breathing Waveforms
        elif command_word == 0x02:
            latest_data["Breathing Rate"] = payload[0]
            #print(f"Breathing Waveform: {payload[0]}")

    # Heart Rate
    elif control_word == 0x85 and command_word == 0x02:
        latest_data["Heart Rate"] = payload[0]


def enable_heart_rate_monitoring():
    """Enables heart rate monitoring."""
    cmd = bytes([0x53, 0x59, 0x85, 0x00, 0x00, 0x01, 0x01, 0x8E, 0x54, 0x43])
    ser.write(cmd)


def set_real_time_mode():
    """Sets the radar to real-time mode."""
    cmd = bytes([0x53, 0x59, 0x84, 0x0F, 0x00, 0x01, 0x00, 0xAE, 0x54, 0x43])
    ser.write(cmd)


def initialize_sensor():
    """Runs initial setup commands for the sensor."""
    enable_heart_rate_monitoring()
    set_real_time_mode()


def read_serial_data():
    """Reads and processes data continuously in the background."""
    buffer = bytearray()
    while True:
        byte = ser.read(1)
        if byte:
            buffer.extend(byte)
            if buffer.endswith(b'\x54\x43') and buffer.startswith(b'\x53\x59'):
                parse_data(buffer)
                buffer.clear()


def start_background_thread():
    """Starts a thread to read sensor data in the background."""
    thread = threading.Thread(target=read_serial_data, daemon=True)
    thread.start()


def get_heart_rate():
    return latest_data["Heart Rate"]


def get_breathing_rate():
    return latest_data["Breathing Rate"]


def get_body_movement():
    return latest_data["Body Movement Intensity"]


def get_distance():
    return latest_data["Distance"]


initialize_sensor()
start_background_thread()