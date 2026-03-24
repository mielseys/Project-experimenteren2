#include <Arduino_BMI270_BMM150.h>

unsigned long previousMillis = 0;
const unsigned long interval = 3000; // 3 seconds

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Magnetometer Data Reader");
  
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  
  Serial.print("Magnetic field sample rate = ");
  Serial.print(IMU.magneticFieldSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Magnetic Field in µT");
  Serial.println("X\tY\tZ");
}

void loop() {
  float x, y, z;
  
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    if (IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(x, y, z);
      
      Serial.print(x);
      Serial.print('\t');
      Serial.print(y);
      Serial.print('\t');
      Serial.println(z);
      
      previousMillis = currentMillis;
    }
  }
}