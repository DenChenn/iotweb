import random
import time

ServerURL = 'https://3.iottalk.tw'
MQTT_broker = '3.iottalk.tw'
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
ODF_list = ['Dummy_Control']
device_id = 'DEN_M'
device_name = 'DEN_M'
exec_interval = 1  # IDF/ODF interval

late_data = []
send_data = 0
start = 0

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))


def Dummy_Sensor():
    global send_data, start
    send_data = random.randint(0, 10000)
    start = time.perf_counter()
    print('Push ', len(late_data), 'data: ', send_data)
    return send_data


def Dummy_Control(data:list):
    global send_data, start
    if data[0] == send_data:
        print('receive ', len(late_data), ' data')
        print('value: ', data[0])
        late_data.append(time.perf_counter() - start)
        if len(late_data) == 100:
            print('Average latency: ', sum(late_data) / len(late_data))
            return
