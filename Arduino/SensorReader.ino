#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>

#define SOIL_MOISTURE_PIN A0
#define RELAISPUMP 2
#define RELAISLIGHT 3
#define DHTPIN 4

#define DHTTYPE DHT22

BH1750 lightSensor;
DHT dhtSensor(DHTPIN, DHTTYPE);
int incoming = 0;


void setup() {
    pinMode(SOIL_MOISTURE_PIN, INPUT);
    pinMode(RELAISPUMP, OUTPUT);
    pinMode(RELAISLIGHT, OUTPUT);

    Serial.begin(9600); /* Begin der Seriellenkommunikation */
    dhtSensor.begin();
    Wire.begin();
    lightSensor.begin();
}

void loop() {

    if (Serial.available() > 0) {
        // Lies das eingehende Byte:
        incoming = Serial.read();

        // Ausgeben:
        //Serial.print("I received: ");
        //Serial.println(incoming);
        switch (incoming)
        {
        case 97: //received a
            getTemperature();
            break;
        case 98: //received b
            getHumidity();
            break;
        case 99: //received c
            getLightSensorData();
            break;
        case 100: //received d
            getSoilMoisture();
            break;
        case 101: //received e
            switchRelaisOn(RELAISLIGHT);
            break;
        case 102: //received f
            switchRelaisOff(RELAISLIGHT);
            break;
        case 103: //received g
            switchRelaisOn(RELAISPUMP);
            break;
        case 104: //received h
            switchRelaisOff(RELAISPUMP);
            break;
        case 105: //received i
            openWindow();
            break;
        case 106: //received j
            closeWindow();
            break;
        default:
            break;
        }
    }
    
}

void getSoilMoisture(){
    Serial.println("Soil Moisture: " + String(analogRead(SOIL_MOISTURE_PIN)));
    delay(10);
}

void switchRelaisOn(int relais){
    digitalWrite(relais,HIGH);
}

void switchRelaisOff(int relais){
    digitalWrite(relais,LOW);
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

void openWindow(){

}

void closeWindow(){

}