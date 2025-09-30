# Anti-Proxy Alcohol Detection System

## 📌 Overview
This project is an **intelligent driver authentication and alcohol detection system** designed to **prevent drunk driving and proxy cheating**.  

Unlike traditional alcohol sensors, which can be bypassed (e.g., by blowing air from someone else), this system integrates:  
- **Arduino Uno** → Acts as the **hardware interface** (sensors, relay, LCD).  
- **Laptop (Python code)** → Works as the **brain** of the system, running advanced face recognition and decision-making.  

---

## ⚡ How It Works
1. **Blow Detection (Arduino):**  
   - BMP180 pressure sensor ensures the driver actually blows into the system.  
   - Prevents cheating with air pumps or fans.  

2. **Alcohol Detection (Arduino):**  
   - MQ-3 sensor measures alcohol level in the breath.  
   - If alcohol > threshold → **vehicle locked immediately**.  

3. **Face Capture (Laptop – Camera 1):**  
   - To capture the driver’s face while blowing.  
   
4. **Continuous Monitoring (Laptop – Camera 2):**  
   - While driving, Camera 2 monitors the driver.  
   - Laptop compares live faces with the stored face encoding.  
   - If face doesn’t match → **relay is turned off, vehicle stopped** (proxy prevented).  

5. **Relay & Ignition Control:**  
   - Arduino only switches the relay (ignition ON/OFF).  
   - It follows commands from the **laptop over serial communication**.  

---

## 🛠 Hardware Components
- Arduino Uno (microcontroller interface)  
- MQ-3 Alcohol Sensor  
- BMP180 Pressure Sensor (blow detection)  
- 16x2 I²C LCD (status display)  
- Relay Module (ignition lock/unlock)  
- LED Indicator (alcohol detected alert)  
- 2 × USB Cameras (one for blowing, one for driver monitoring)  
- Jumper wires, breadboard, power supply  

---

## 💻 Software & Libraries

### Arduino (Embedded Layer):
- `Wire.h`  
- `Adafruit_Sensor.h`  
- `Adafruit_BMP085_U.h`  
- `LiquidCrystal_I2C.h`  

### Python (Laptop – Brain Layer):
- `opencv-python` → Camera input & image processing  
- `face_recognition` → Face encoding & recognition  
- `numpy` → Mathematical operations & distance calculation  
- `pyserial` → Communication with Arduino over USB  
- `time` → Timing and delays  
- `os` (optional if used) → File handling for saving images  

---

## 🔌 Circuit Connections

**MQ-3 Alcohol Sensor**  
- VCC → 5V  
- GND → GND  
- AO → A0  

**BMP180 (I²C)**  
- VCC → 3.3V  
- GND → GND  
- SDA → A4  
- SCL → A5  

**LCD (16x2 I²C)**  
- VCC → 5V  
- GND → GND  
- SDA → A4  
- SCL → A5  

**Relay Module**  
- VCC → 5V  
- GND → GND  
- IN → D8  

**LED**  
- Anode → D9  
- Cathode → Resistor → GND  

---

## 🚦 System Workflow

---

## 📂 Repository Contents
- `arduino_code/` → Arduino sketch (sensors, LCD, relay, serial communication)  
- `python_code/` → Python script (face recognition, decision making, relay commands)  
- `circuit_diagram/` → Circuit schematic  
- `media/` → Photos & demo videos of the project  
- `README.md` → Documentation (this file)  

---

## 🗓️ Project Timeline
- **October 2024 (End):** Project designed and implemented.  
- **September 2025:** Documentation and GitHub release.  

---

## 👨‍💻 Author
Developed by **Shaurya Garg**  
[LinkedIn](https://www.linkedin.com/in/shaurya-garg-445a93386/) |  

---

## 📜 License
Licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.  
Use for research & education is allowed, commercial use is not.  
