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


def callback(ch, method, properties, body):
    data = json.loads(body)
    #ser.write(b"g")
    print('Received: {}'.format(data))


channel.basic_consume(queue='sciot.action', on_message_callback=callback, auto_ack=True)
print('Waiting for messages')
channel.start_consuming()