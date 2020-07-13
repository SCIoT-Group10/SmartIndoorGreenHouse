import json
import pika
import threading
import PySimpleGUI as sg
import datetime
import time as ttime
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

temperature_threshold = [23.0, 30.0]
humidity_threshold = [50, 70]
lightLevel_threshold = [100, 400]
soilMoisture_threshold = [700, 400]
time_threshold = [8, 20]

flags = [['brightnessHigh', False],
         ['brightnessLow', False],
         ['moistureHigh', False],
         ['moistureLow', False],
         ['waterHigh', False],
         ['waterLow', False],
         ['temperatureHigh', False],
         ['temperatureLow', False],
         ['humidityHigh', False],
         ['humidityLow', False],
         ['day', False],
         ['night', False],
         ['pumpOn', False],
         ['pumpOff', True],
         ['lightsOn', False],
         ['lightsOff', True],
         ['windowOpen', False],
         ['windowClosed', True]]

localtime = datetime.datetime.now()

time = ''
temperature = 0.0
humidity = 0.0
lightLevel = 0.0
waterLevel = 'FULL'
soilMoisture = 0

pddl_Files = ["temperatureLowProblem.pddl", "temperatureHighProblem.pddl", "humidityLowProblem.pddl",
              "humidityHighProblem.pddl", "brigthnessLowProblem.pddl", "brigthnessHighProblem.pddl",
              "moistureLowProblem.pddl"]


def setFlags():
    global flags
    if localtime.hour > time_threshold[0] & localtime.hour < time_threshold[1]:
        for flag in flags:
            if flag[0] == 'day':
                flag[1]=True
            if flag[0] == 'night':
                flag[1] = False
    if temperature < temperature_threshold[0]:
        for flag in flags:
            if flag[0] == 'temperatureLow':
                flag[1] = True
            if flag[0] == 'temperatureHigh':
                flag[1] = False
    elif temperature > temperature_threshold[1]:
        for flag in flags:
            if flag[0] == 'temperatureHigh':
                flag[1] = True
            if flag[0] == 'temperatureLow':
                flag[1] = False
    if humidity < humidity_threshold[0]:
        for flag in flags:
            if flag[0] == 'humidityLow':
                flag[1] = True
            if flag[0] == 'humidityHigh':
                flag[1] = False
    elif humidity > humidity_threshold[1]:
        for flag in flags:
            if flag[0] == 'humidityHigh':
                flag[1] = True
            if flag[0] == 'humidityLow':
                flag[1] = False
    if lightLevel < lightLevel_threshold[0]:
        for flag in flags:
            if flag[0] == 'brightnessLow':
                flag[1] = True
            if flag[0] == 'brightnessHigh':
                flag[1] = False
    elif lightLevel > lightLevel_threshold[1]:
        for flag in flags:
            if flag[0] == 'brightnessHigh':
                flag[1] = True
            if flag[0] == 'brightnessLow':
                flag[1] = False
    if soilMoisture > soilMoisture_threshold[0]:
        for flag in flags:
            if flag[0] == 'moistureLow':
                flag[1] = True
            if flag[0] == 'moistureHigh':
                flag[1] = False

    print(flags)


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

    setFlags()

    for problem in pddl_Files:
        precondition, effects = solve(problem)
        for pre in precondition:
            for flag in flags:
                if pre == flag:
                        print(pre)

        for effect in effects:
            for flag in flags:
                if effects[0] == flags[0]:
                    flags[flag] = effect

    # if localtime.hour > time_threshold[0] & localtime.hour < time_threshold[1]:
    #   if temperature < temperature_threshold[0]:
    #       preconditions, effects = solve('humidityLowProblem.pddl')
    # print(preconditions)

    print(actions)

    data = {
        "time": time,
        "operation": actions
    }
    jsonData = json.dumps(data)
    channel2.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.action.12345', body=jsonData)
    pass


def getPreconditions(action_string):
    preconditions = []
    z = action_string.split(":")
    for a in z:
        if a.startswith('precondition'):
            b = a.split('(')
            b_cleaned = []
            for i in range(len(b)):
                b[i] = b[i].replace('\n', '')
                if len(b[i]) > 0:
                    b[i] = b[i].replace(')', '').replace(' ', '')
                    b_cleaned.append(b[i])
            for i in range(len(b_cleaned)):
                if i > 1:
                    if not b_cleaned[i] == 'not':
                        if b_cleaned[i - 1] == 'not':
                            preconditions.append([b_cleaned[i], False])
                        else:
                            preconditions.append([b_cleaned[i], True])
    return preconditions
    pass


def getEffects(action_string):
    effects = []
    z = action_string.split(":")
    for a in z:
        if a.startswith('effect'):
            b = a.split('(')
            b_cleaned = []
            for i in range(len(b)):
                b[i] = b[i].replace('\n', '')
                if len(b[i]) > 0:
                    b[i] = b[i].replace(')', '').replace(' ', '')
                    b_cleaned.append(b[i])
            for i in range(len(b_cleaned)):
                if i > 1:
                    if not b_cleaned[i] == 'not':
                        if b_cleaned[i - 1] == 'not':
                            effects.append([b_cleaned[i], False])
                        else:
                            effects.append([b_cleaned[i], True])
    return effects
    pass


def solve(problem):
    planningData = {'domain': open("greenHouseDomain.pddl", 'r').read(),
                    'problem': open(problem, 'r').read()}
    response = requests.post('http://solver.planning.domains/solve', json=planningData).json()
    for act in response["result"]["plan"]:
        action_string = act['action']
        preconditions = getPreconditions(action_string)
        effects = getEffects(action_string)

        return preconditions, effects


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
