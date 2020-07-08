import time
import pika
import serial

timeout = 30

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
time.sleep(5)

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.3.27', 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)


def main():
    while True:
        sensorValues = getSensorData()

        json = json.dumps(sensorValues)

        message = time.ctime() + json
        channel.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.temperature.12345', body=message)
        print('Sent ' + message)
        time.sleep(timeout)


def getTemperature():
    ser.write(b"a")
    line = ser.readline().decode('utf-8').rstrip()
    return float(line)


def getHumidity():
    ser.write(b"b")
    line = ser.readline().decode('utf-8').rstrip()
    return float(line)


def getLightLevel():
    ser.write(b"c")
    line = ser.readline().decode('utf-8').rstrip()
    return float(line)


def getSoilMoisture():
    ser.write(b"d")
    line = ser.readline().decode('utf-8').rstrip()
    return float(line)


def getWaterLevel():
    return "full"


def getSensorData():
    sensorValues = SensorValues()
    sensorValues.temperature = getTemperature()
    sensorValues.humidity = getHumidity()
    sensorValues.lightLevel = getLightLevel()
    sensorValues.soilMoisture = getSoilMoisture()
    sensorValues.waterLevel = getWaterLevel()

    return sensorValues


class SensorValues:
    temperature = 0.0
    humidity = 0.0
    soilMoisture = 0.0
    lightLevel = 0.0
    waterLevel = "empty"
