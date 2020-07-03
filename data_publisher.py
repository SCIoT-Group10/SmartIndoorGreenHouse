import time
import pika

timeout = 1

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.3.27', 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)

while True:
  temperature = 15
  humidity = 49
  message = time.ctime() + ' Temperature = ' + str(temperature) + ' C, humidity = ' + str(humidity) + ' %'
  channel.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.temperature.12345', body=message)
  print('Sent ' + message)
  time.sleep(timeout)
