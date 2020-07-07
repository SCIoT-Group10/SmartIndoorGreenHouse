#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>

#define SOIL_MOISTURE_PIN A0
#define RELAIS1 2
#define RELAIS2 3
#define DHTPIN 4

#define DHTTYPE DHT22

BH1750 lightSensor;
DHT dhtSensor(DHTPIN, DHTTYPE);


void setup() {
    pinMode(SOIL_MOISTURE_PIN, INPUT);
    pinMode(RELAIS1, OUTPUT);
    pinMode(RELAIS2, OUTPUT);

    Serial.begin(9600); /* Begin der Seriellenkommunikation */
    dhtSensor.begin();
    //Wire.begin();
    //lightSensor.begin();
}

void loop() {
    //switchRelais();
    getSoilMoisture();
    //getLightSensorData();
    getTemperature();
    getHumidity();
    delay(5000);
    
}

void getSoilMoisture(){
    Serial.println("Soil Moisture: " + String(analogRead(SOIL_MOISTURE_PIN)));
    delay(10);
}

void switchRelais(){
    digitalWrite(RELAIS2,HIGH);
    delay(2000);
    digitalWrite(RELAIS2,LOW);
}

void getLightSensorData(){
    float lux = lightSensor.readLightLevel();
    Serial.println("Light level: " + String(lux) + " lx");
    delay(10);
}

void getTemperature(){
    float Temperatur = dhtSensor.readTemperature();
    Serial.println("Temperatur: " + String(Temperatur) +"°C");
    
}

void getHumidity(){
    float Luftfeuchtigkeit = dhtSensor.readHumidity();
    Serial.println("Luftfeuchtigkeit: " + String(Luftfeuchtigkeit) +"%");
}