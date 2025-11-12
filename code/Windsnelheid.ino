const int pinSignal = A0;   // analog input pin
const float Vref = 5.0;     // Arduino Uno reference voltage (assuming default)
const int ADCmax = 1023;    // 10-bit ADC
const float maxWindSpeed = 30.0;  // 0-5V corresponds to 0-30 m/s

void setup() {
  Serial.begin(115200);
  pinMode(pinSignal, INPUT);
  Serial.println("YX-DFS2 Wind Speed Sensor Test");
}

void loop() {
  int raw = analogRead(pinSignal);
  float voltage = raw * (Vref / (float)ADCmax);
  float windSpeed_m_s = (voltage / 5.0) * maxWindSpeed;
  float windSpeed_kmh = windSpeed_m_s * 3.6;

  Serial.print("Raw ADC = ");
  Serial.print(raw);
  Serial.print(", Voltage = ");
  Serial.print(voltage, 3);
  Serial.print(" V, Wind speed = ");
  Serial.print(windSpeed_m_s, 2);
  Serial.print(" m/s (");
  Serial.print(windSpeed_kmh, 2);
  Serial.println(" km/h)");

  delay(500);  // read every 0.5 seconds
}
