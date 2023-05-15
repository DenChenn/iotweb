import DAN
import time
from tqdm import tqdm

ServerURL = 'https://3.iottalk.tw'
reg_addr = None

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name'] = 'DEN'

DAN.device_registration_with_retry(ServerURL, reg_addr)
print('dm_name is ', DAN.profile['dm_name'])
print('Server is ', ServerURL)


def handle_exception(ex):
    print(ex)
    if str(ex).find('mac_addr not found:') != -1:
        print('Reg_addr is not found. Try to re-register...')
        DAN.device_registration_with_retry(ServerURL, reg_addr)
    else:
        print('Connection failed due to unknown reasons.')
        time.sleep(1)


while True:
    try:
        latency = []
        idf_name, odf_name = 'Dummy_Sensor', 'Dummy_Control'

        # wait for iottalk to start
        time.sleep(15)
        for data in tqdm(range(100)):
            print(data)
            try:
                start = time.perf_counter()
                print('start pushing data: '+str(data))
                DAN.push(idf_name, data)
                print('end pushing data: '+str(data))
                time.sleep(2)
                while True:
                    try:
                        print('start pulling data')
                        catch = DAN.pull(odf_name)
                        print('end pulling data')
                        print('catch: ', catch)
                        if catch is not None and catch == data:
                            latency.append(time.perf_counter() - start)
                            break

                    except Exception as e:
                        handle_exception(e)

            except Exception as e:
                handle_exception(e)

        print('Average latency: ', sum(latency) / len(latency))

    except Exception as e:
        handle_exception(e)

    time.sleep(3)
