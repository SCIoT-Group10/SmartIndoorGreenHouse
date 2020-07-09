#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>
#include <Stepper.h>

#define SOIL_MOISTURE_PIN A0
#define RELAISPUMP 3
#define RELAISLIGHT 2
#define DHTPIN 4

#define DHTTYPE DHT22

BH1750 lightSensor;
DHT dhtSensor(DHTPIN, DHTTYPE);
int incoming = 0;

const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 5, 7, 6, 8);


void setup() {
    pinMode(SOIL_MOISTURE_PIN, INPUT);
    pinMode(RELAISPUMP, OUTPUT);
    pinMode(RELAISLIGHT, OUTPUT);

    digitalWrite(RELAISLIGHT,HIGH);
    digitalWrite(RELAISPUMP,HIGH);

    myStepper.setSpeed(15);

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
            getWaterLevel();
            break;
        case 102: //received f
            switchRelaisOn(RELAISLIGHT);
            break;
        case 103: //received g
            switchRelaisOff(RELAISLIGHT);
            break;
        case 104: //received h
            switchRelaisOn(RELAISPUMP);
            break;
        case 105: //received i
            switchRelaisOff(RELAISPUMP);
            break;
        case 106: //received j
            openWindow();
            break;
        case 107: //received k
            closeWindow();
            break;
        default:
            break;
        }
    }
    
}

void getSoilMoisture(){
    Serial.println(String(analogRead(SOIL_MOISTURE_PIN)));
    delay(10);
}

void switchRelaisOn(int relais){
    digitalWrite(relais,LOW);
}

void switchRelaisOff(int relais){
    digitalWrite(relais,HIGH);
}

void getLightSensorData(){
    float lux = lightSensor.readLightLevel();
    Serial.println(String(lux));
    delay(10);
}

void getTemperature(){
    float temperature = dhtSensor.readTemperature();
    Serial.println(String(temperature));
    
}

void getHumidity(){
    float humidity = dhtSensor.readHumidity();
    Serial.println(String(humidity));
}

void getWaterLevel(){

}

void openWindow(){
    for(int i=0; i< stepsPerRevolution; i++){
        myStepper.step(1);
    }
}

void closeWindow(){
    for(int i=0; i< stepsPerRevolution; i++){
        myStepper.step(-1);
    }
}