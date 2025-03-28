# INF2009-Project

This repository contains the code and configurations for setting up and running various applications on Raspberry Pi 4 and Raspberry Pi 5 devices. Follow the instructions below to properly set up each component.

## Cloning the Repository

Begin by cloning this repository onto both the Raspberry Pi 4 and Raspberry Pi 5 devices:

```bash
git clone https://github.com/Afiq2200546/INF2009-Project.git
```

---

## Raspberry Pi 4 Setup

### Body Temperature Application:

Navigate to the `Pi 4/body_temp` directory:

```bash
cd INF2009-Project/Pi 4/body_temp
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

### DHT22 Application:

Navigate to the `Pi 4/dht22` directory:

```bash
cd ../dht22
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## Raspberry Pi 5 Setup

### MagicMirror Installation:

Follow the official MagicMirror installation guide available at [MagicMirror² Documentation](https://docs.magicmirror.builders/).

### MagicMirror MQTT Module Installation:

Navigate to the MagicMirror modules directory:

```bash
cd ~/MagicMirror/modules
```

Clone the MMM-MQTT repository:

```bash
git clone https://github.com/ottopaulsen/MMM-MQTT.git
```

Navigate to the MMM-MQTT directory:

```bash
cd MMM-MQTT
```

Install the necessary dependencies:

```bash
npm install
```

For detailed configuration, refer to the [MMM-MQTT GitHub Repository](https://github.com/ottopaulsen/MMM-MQTT).

### Configuration File Setup:

Copy the `config.js` file from `Pi 5/MagicMirror/config/` directory of this repository to your local MagicMirror config directory:

```bash
cp INF2009-Project/Pi 5/MagicMirror/config/config.js ~/MagicMirror/config/
```

### Ollama Installation and Qwen2.5:3B Model Download:

Install Ollama on the Raspberry Pi. Please refer to the [official Ollama documentation](https://ollama.ai/) for Raspberry Pi installation instructions.

After installing Ollama, download the Qwen2.5:3B model. Detailed steps can be found in the Ollama documentation.

---

## Setting Up and Running Python Scripts

For each of the following directories, perform the steps below:

### Directories:
- `Pi 5/central_code`
- `Pi 5/heart_rate`
- `Pi 5/stt`
- `Pi 5/web_interface_2`

### Steps:

Navigate to the directory:

```bash
cd INF2009-Project/<directory_name>
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the respective Python scripts as needed. For example:

```bash
python app.py
```

> **Note:** Replace `<directory_name>` with the actual directory path. Ensure you run the appropriate script files (`app.py`, `test_mic.py`, etc.) as required for your setup.

By following these steps, you should have all components set up and running on your Raspberry Pi 4 and Raspberry Pi 5 devices.

