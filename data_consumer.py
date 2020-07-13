import json
import pika
import threading
import PySimpleGUI as sg
import datetime
import requests

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.3.27', 5672, '/', credentials))
channel = connection.channel()
channel2 = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)
channel2.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)

channel.queue_declare(queue='sciot.temperature')

channel.queue_bind(queue='sciot.temperature', exchange='sciot.topic', routing_key='u38.0.353.*.temperature.*')

planningData = {'domain': open('greenHouseDomain.pddl', 'r').read(),
                'problem': open('greenHouseProblem.pddl', 'r').read()}

precondition_Light = False
precondition_Pump = False
precondition_Window = False

temperature_threshold = [23.0, 30.0]
humidity_threshold = [50, 70]
lightLevel_threshold = [100, 400]
soilMoisture_threshold = [700, 400]
time_threshold = [8, 20]

localtime = datetime.datetime.now()

time = ''
temperature = 0.0
humidity = 0.0
lightLevel = 0.0
waterLevel = 'FULL'
soilMoisture = 0


def planning(data):
    actions = []

    global localtime
    global time
    global temperature
    global humidity
    global lightLevel
    global waterLevel
    global soilMoisture

    localtime = datetime.datetime.now()
    time = data['time']
    temperature = data['temperature']
    humidity = data['humidity']
    lightLevel = data['lightLevel']
    waterLevel = data['waterLevel']
    soilMoisture = data['soilMoisture']

    if localtime.hour > time_threshold[0] & localtime.hour < time_threshold[1]:
        if temperature < temperature_threshold[0]:
            solve('temperatureLowProblem.pddl')

            actions.append("openWindow")
        elif temperature > temperature_threshold[1]:
            solve('temperatureHighProblem.pddl')
            actions.append("closeWindow")

        if humidity < humidity_threshold[0]:
            solve('humidityLowProblem.pddl')
            actions.append("openWindow")
        elif humidity > humidity_threshold[1]:
            solve('humidityHighProblem.pddl')
            actions.append("closeWindow")

        if lightLevel < lightLevel_threshold[0]:
            solve('brigthnessLowProblem.pddl')
            actions.append("lightsOn")
        elif lightLevel > lightLevel_threshold[1]:
            solve('brigthnessHighProblem.pddl')
            actions.append("lightsOff")

        if soilMoisture > soilMoisture_threshold[0]:
            solve("moistureLowProblem.pddl")
            actions.append("pump")

    # for act in actions:
    #   print(act['precondition'])

    print(actions)

    data = {
        "time": time,
        "operation": actions
    }
    jsonData = json.dumps(data)
    channel2.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.action.12345', body=jsonData)
    pass


def getPreconditions(action_string):
    pass


def getEffects(action_string):
    pass


def solve(problem):
    #planningData = {'domain': open("greenHouseDomain.pddl", 'r').read(),
    #                'problem': open(problem, 'r').read()}
    #response = requests.post('http://solver.planning.domains/solve', json=planningData).json()

    #for act in response['result']['plan']:
    #    action_string = act['action']
    #    getPreconditions(action_string)
    #    getEffects(action_string)
    print('solve')


def callback(ch, method, properties, body):
    data = json.loads(body)
    planning(data)
    print('Received: {}'.format(data))


def ui_thread(name):
    global temperature_threshold
    global humidity_threshold
    global lightLevel_threshold
    global soilMoisture_threshold
    global time_threshold

    layout = [
        [sg.Text('Last Values:')],
        [sg.Text('Time: ', size=(15, 1)), sg.Text(str(time), key='_TIME_')],
        [sg.Text('Temperature:', size=(15, 1)), sg.Text(str(temperature), key='_TEMPERATURE_')],
        [sg.Text('Humidity:', size=(15, 1)), sg.Text(str(humidity), key='_HUMIDITY_')],
        [sg.Text('Lightlevel:', size=(15, 1)), sg.Text(str(lightLevel), key='_LIGHT_')],
        [sg.Text('Waterlevel:', size=(15, 1)), sg.Text(waterLevel, key='_WATER_')],
        [sg.Text('Soil Moisture:', size=(15, 1)), sg.Text(soilMoisture, key='_SOIL_')],
        [sg.Button('Get latest Values')],
        [sg.Text()],
        [sg.Text('Please enter a Thresholts for the following values')],
        [sg.Text('Temperature Low', size=(15, 1)), sg.InputText(temperature_threshold[0]),
         sg.Text('Temperature High', size=(15, 1)), sg.InputText(temperature_threshold[1])],
        [sg.Text('Humidity Low', size=(15, 1)), sg.InputText(humidity_threshold[0]),
         sg.Text('Humidity High', size=(15, 1)), sg.InputText(humidity_threshold[1])],
        [sg.Text('LightLevel Low', size=(15, 1)), sg.InputText(lightLevel_threshold[0]),
         sg.Text('LightLevel High', size=(15, 1)), sg.InputText(lightLevel_threshold[1])],
        [sg.Text('SoilMoisture Low', size=(15, 1)), sg.InputText(soilMoisture_threshold[0]),
         sg.Text('SoilMoisture High', size=(15, 1)), sg.InputText(soilMoisture_threshold[1])],
        [sg.Text('Time Morning', size=(15, 1)), sg.InputText(time_threshold[0]),
         sg.Text('Time Evening', size=(15, 1)), sg.InputText(time_threshold[1])],
        [sg.Submit()]]

    # Create the Window
    window = sg.Window('Smart Greenhouse Control', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.Read()

        window['_TIME_'](str(time))
        window['_TEMPERATURE_'](str(temperature))
        window['_HUMIDITY_'](str(humidity))
        window['_LIGHT_'](str(lightLevel))
        window['_WATER_'](str(waterLevel))
        window['_SOIL_'](str(soilMoisture))

        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == 'Get latest Values':
            window['_TIME_'](str(time))
            window['_TEMPERATURE_'](str(temperature))
            window['_HUMIDITY_'](str(humidity))
            window['_LIGHT_'](str(lightLevel))
            window['_WATER_'](str(waterLevel))
            window['_SOIL_'](str(soilMoisture))
        temperature_threshold = [float(values[0]), float(values[1])]
        humidity_threshold = [float(values[2]), float(values[3])]
        lightLevel_threshold = [float(values[4]), float(values[5])]
        soilMoisture_threshold = [float(values[6]), float(values[7])]
        time_threshold = [int(values[8]), int(values[9])]

    window.close()


print(time)

x = threading.Thread(target=ui_thread, args=(1,))
x.start()
channel.basic_consume(queue='sciot.temperature', on_message_callback=callback, auto_ack=True)
print('Waiting for messages')
channel.start_consuming()
