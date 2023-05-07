import DAN
import random
import time

ServerURL = 'https://3.iottalk.tw'
Reg_addr = None

mac_addr = 'DEN_MAC_1'
Reg_addr = mac_addr   # Note that the mac_addr generated in DAN.py always be the same cause using UUID !

DAN.profile['dm_name'] = 'DEN_Dummy_253'   # you can change this but should also add the DM in server
DAN.profile['df_list'] = ['Slider', 'Color_I', 'Dmy_d253', 'Dummy_Control']
DAN.profile['d_name'] = "DEN." + str(random.randint(100, 999)) + "_" + DAN.profile['dm_name']
DAN.device_registration_with_retry(ServerURL, Reg_addr) 
print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL)

while True:
    try:
        output = DAN.pull('Dummy_Control')
        if output:
            print(output[0])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)

    time.sleep(0.2)
