import random
import time

### The registeration api url, you can use IP or Domain.
api_url = 'https://iottalk2.tw/csm'  # default

## [OPTIONAL] If not given or None, server will auto-generate.
##device_name = 'DEN_v2'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
# device_addr = "{:012X}".format(getnode())
# device_addr = "..."

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
# persistent_binding = True

### [OPTIONAL] If not given or None, this device will be used by anyone.
# username = 'myname'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Dummy_Device'

### The input/output device features, please check IoTtalk document.
idf_list = ['DummySensor-I']
odf_list = ['DummyControl-O']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval
interval = {
    'Dummy_Sensor': 0.5,  # assign feature interval
}

late_data = []
send_data = 0
start = 0

def on_register(dan):
    print('register successfully')


def DummySensor_I():
    global send_data, start
    send_data = random.randint(0, 10000)
    start = time.perf_counter()
    print('Push ', len(late_data), 'data: ', send_data)
    return send_data

def DummyControl_O(data: list):
    global send_data, start
    if data[0] == send_data:
        print('receive ', len(late_data), ' data')
        print('value: ', data[0])
        late_data.append(time.perf_counter() - start)
        if len(late_data) == 100:
            print('Average latency: ', sum(late_data) / len(late_data))
            return
