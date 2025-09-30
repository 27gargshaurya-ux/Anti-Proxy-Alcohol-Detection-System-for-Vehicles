# Anti-Proxy Alcohol Detection System for Vehicles

## 📌 Overview
This project is an **advanced alcohol detection and driver authentication system** designed to enhance road safety. Unlike traditional alcohol sensors that can be bypassed, this system prevents **proxy attempts** by combining **alcohol detection with face verification**.

- **Alcohol Detection:** Uses an MQ-3 sensor to measure alcohol concentration in the driver’s breath.  
- **Blow Detection:** A BMP180 pressure sensor ensures that the driver actually blows into the system before alcohol measurement.  
- **Proxy Prevention with Face Matching:**  
  - Camera 1 captures the image of the person blowing air.  
  - Camera 2 continuously monitors the driver’s face while driving.  
  - The system compares both faces to ensure the same person is driving — preventing proxy tests.  
- **Vehicle Control:** A relay is used to enable/disable the ignition depending on the results.  
- **Visual Feedback:** A 16x2 I²C LCD and LED provide clear system status.  

---

## ⚡ Features
- Detects if alcohol is present in the driver’s breath.  
- Detects **air blow pressure** (no bypass with fake air pumps).  
- Captures the photo of the person blowing.  
- Performs **real-time face recognition** to ensure the same person is driving.  
- Relay module controls ignition system (engine locked if alcohol detected or faces don’t match).  
- Displays results on LCD and logs through Serial Monitor.  

---

## 🛠 Hardware Components
- Arduino Uno / compatible board  
- MQ-3 Alcohol Sensor  
- BMP180 Pressure Sensor (for blow detection)  
- 16x2 I²C LCD  
- Relay Module (for ignition lock)  
- LED + Resistor (status indicator)  
- 2 × USB Cameras (one for blowing, one for driver monitoring)  
- Jumper wires, breadboard, power supply  

---

## 💻 Software & Libraries
**Arduino IDE:**  
- `Wire.h`  
- `Adafruit_Sensor.h`  
- `Adafruit_BMP085_U.h`  
- `LiquidCrystal_I2C.h`  

**Python (PC side for face matching):**  
- `opencv-python`  
- `face_recognition`  
- `numpy`  
- `pyserial`  

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

**LCD (I²C, 16x2)**  
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
1. **Blow Detection:** BMP180 verifies that the driver blows into the system.  
2. **Alcohol Detection:** MQ-3 measures alcohol content.  
3. **Face Capture (Camera 1):** Captures the person blowing air.  
4. **Face Monitoring (Camera 2):** Continuously checks the driver’s face.  
5. **Comparison:** If faces match *and* no alcohol is detected → relay ON (vehicle starts).  
6. If alcohol is detected OR faces do not match → relay OFF (vehicle locked).  

---

## 📂 Repository Contents
- `arduino_code/` → Arduino sketch for MQ-3, BMP180, LCD, Relay  
- `python_code/` → Python script for dual-camera face matching and relay control  
- `circuit_diagram/` → Circuit schematic  
- `media/` → Photos & demo videos of the project  
- `README.md` → Documentation (this file)  

---

## 📜 License
This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** License.  
You are free to use and modify the code for learning and research, but **commercial use is not permitted**.  
[View License](https://creativecommons.org/licenses/by-nc/4.0/)  

---

## 🗓️ Project Timeline
- **October 2024 (End):** Project designed and implemented.  
- **September 2025:** Documentation, cleanup, and upload to GitHub.  

---

## 👨‍💻 Author
Developed by **Shaurya Garg**  
[LinkedIn](https://www.linkedin.com/in/shaurya-garg-445a93386/) 
---
