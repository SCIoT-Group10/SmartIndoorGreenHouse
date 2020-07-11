import json
import serial
import pika
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
time.sleep(5)

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.3.42', 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)

channel.queue_declare(queue='sciot.action')

channel.queue_bind(queue='sciot.action', exchange='sciot.topic', routing_key='u38.0.353.*.action.*')

lightOn = False
windowOpen = False


def callback(ch, method, properties, body):
    data = json.loads(body)
    time = data['time']
    operation = data['operation']

    if operation == "lightsOff":
        lightsOff()

    if operation == "lightsOn":
        lightsOn()

    # TODO: check time
    # TODO: switch case
    #print('Received: {}'.format(data['operation']))


def lightsOn():
    global lightOn
    if not lightOn:
        lightOn = True
        ser.write(b"f")
        print('Lights On')


def lightsOff():
    global lightOn
    if lightOn:
        lightOn = True
        ser.write(b"g")
        print('Lights Off')


def pump():
    ser.write(b"h")
    time.sleep(10)
    ser.write(b"i")


def openWindow():
    global windowOpen
    if not windowOpen:
        windowOpen = True
        ser.write(b"j")
        print('Window open')


def closeWindow():
    global windowOpen
    if windowOpen:
        windowOpen = False
        ser.write(b"k")
        print('Window closed')


channel.basic_consume(queue='sciot.action', on_message_callback=callback, auto_ack=True)
print('Waiting for messages')
channel.start_consuming()
