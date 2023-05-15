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

        # wait for iottalk to start and click refresh
        time.sleep(20)
        for data in tqdm(range(100)):
            try:
                start = time.perf_counter()
                DAN.push(idf_name, data)
                while True:
                    try:
                        catch = DAN.pull(odf_name)
                        if catch is not None and catch[-1] is not None and catch[-1] == data:
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
