import time
import pika
import serial
import json

timeout = 30

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
time.sleep(5)

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.3.42', 5672, '/', credentials))
channel = connection.channel()
channel2 = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)
channel2.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)

channel.queue_declare(queue='sciot.action')


def getSensorData():
    data = {
        "time": time.ctime(),
        "temperature": getTemperature(),
        "humidity": getHumidity(),
        "lightLevel": getLightLevel(),
        "soilMoisture": getSoilMoisture(),
        "waterLevel": getWaterLevel()
    }
    return data


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
    ser.write(b"e")
    line = ser.readline().decode('utf-8').rstrip()
    return line

def callback(ch, method, properties, body):
    data = json.loads(body)
    print('Received: {}'.format(data))

if __name__ == '__main__':
    channel.basic_consume(queue='sciot.temperature', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    while True:
        sensorValues = getSensorData()

        jsonData = json.dumps(sensorValues)

        channel.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.temperature.12345', body=jsonData)
        time.sleep(timeout)
