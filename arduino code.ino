#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <LiquidCrystal_I2C.h> // Include the I2C LCD library

// BMP180 pressure sensor
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

// MQ-3 alcohol sensor pin
const int mq3Pin = A0;  
const int alcoholThreshold = 800;  // Adjust threshold for alcohol detection
const float blowThreshold = 0.4;   // Threshold for detecting a blow in hPa
const float resetThreshold = 0.3;  // Threshold for resetting detection

// Flags and state variables
float lastPressure = 0.0;
bool blowDetected = false;

// Pins for LED and relay
const int ledPin = 9;
const int relayPin = 8; 

// Initialize the LCD, change the address (0x27) if needed for your LCD
LiquidCrystal_I2C lcd(0x26, 16, 2); // Address, Columns, Rows

void setup() {
  Serial.begin(9600);

  // Initialize BMP180 sensor
  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP180 sensor, check wiring!");
    while (1); // Halt if sensor initialization fails
  }

  // Read initial pressure
  sensors_event_t event;
  bmp.getEvent(&event);
  lastPressure = event.pressure; 
   // Pressure in hPa

  // Set up pins
  pinMode(ledPin, OUTPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  digitalWrite(relayPin, LOW);

  // Initialize LCD
  lcd.begin(16, 2);  // Initialize with the number of columns and rows
  lcd.backlight(); // Turn on the backlight
  lcd.clear(); // Clear the LCD
  lcd.setCursor(0, 0); // Set cursor to the first row
  lcd.print("BLOW AIR"); // Display starting message
  delay(2000); // Display for 2 seconds
}

void loop() {
  // Read the current pressure
  sensors_event_t event;
  bmp.getEvent(&event);
  float currentPressure = event.pressure;

  // Check if blow detected based on pressure change
  if (!blowDetected && (currentPressure - lastPressure >= blowThreshold)) {
    Serial.println("DETECTED");  // Send "DETECTED" if blow detected
    blowDetected = true;         // Prevent multiple detections until reset
    delay(500);                  // Short delay before checking alcohol

    // Check alcohol level only if blow is detected
    int alcoholLevel = analogRead(mq3Pin);
    if (alcoholLevel > alcoholThreshold) {
      Serial.println("ALCOHOL_DETECTED");  // Send "ALCOHOL_DETECTED" to laptop
      digitalWrite(ledPin, HIGH);          // Turn on LED if alcohol detected

      // Display message on LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("ALCOHOL DETECTED"); // Display message
    } else {
      Serial.println("NO_ALCOHOL");        // Send "NO_ALCOHOL" if no alcohol
      digitalWrite(ledPin, LOW);           // Ensure LED is off if no alcohol

      // Clear LCD if no alcohol detected
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("NO ALCOHOL");
      delay(2000);
      lcd.clear();
      lcd.print("MATCHING FACE"); // Display message
    }
    delay(2000); // Hold the message for 2 seconds
  } else {
    Serial.println("NOT_DETECTED"); // Send "NOT_DETECTED" if no blow
  }
  
  // Reset blow detection if pressure stabilizes
  if (blowDetected && abs(currentPressure - lastPressure) < resetThreshold) {
    blowDetected = false;
    Serial.println("Blow detection reset.");
  }

  // Listen for commands from Python to control the relay
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command == "RELAY_ON") {
      digitalWrite(relayPin, HIGH);  // Turn on relay
      Serial.println("Relay is ON");
    } else if (command == "RELAY_OFF") {
      digitalWrite(relayPin, LOW);   // Turn off relay
      Serial.println("Relay is OFF");
    }
  }

  // Update last pressure and add delay for stability
  lastPressure = currentPressure;
  delay(400);
}
