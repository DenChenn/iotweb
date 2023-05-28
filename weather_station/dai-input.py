import DAN
import datetime
import sys  # for using a Thread to read keyboard INPUT
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ServerURL = 'https://2.iottalk.tw'

Reg_addr = None

mac_addr = 'CD8_0812253_weather_station'

Reg_addr = mac_addr  # Note that the mac_addr generated in DAN.py always be the same cause using UUID !
DAN.profile['dm_name'] = '0812253_weather_station'
DAN.profile['df_list'] = ['date', 'hum', 'rain', 'sunlight', 'temp', 'visible', 'weather', 'wind_direction',
                          'wind_speed']
DAN.profile['d_name'] = mac_addr
DAN.device_registration_with_retry(ServerURL, Reg_addr)
print("dm_name is ", DAN.profile['dm_name'])
print("Server is ", ServerURL)

allDead = False

date = []
hum = []
rain = []
sunlight = []
temp = []
visible = []
weather = []
wind_direction = []
wind_speed = []


def do_read():
    date.clear()
    hum.clear()
    rain.clear()
    sunlight.clear()
    temp.clear()
    visible.clear()
    weather.clear()
    wind_direction.clear()
    wind_speed.clear()

    region = 'Tainan'
    url = 'https://www.cwb.gov.tw/V8/C/W/OBS_Station.html?ID=46741'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features='lxml')
    tbody = soup.find('tbody', {'id': 'obstime'})
    trs = tbody.find_all('tr')
    year = str(datetime.datetime.now().year)

    for tr in trs:
        d = tr.th.text
        d = year + d

        date.append(datetime.datetime.strptime(d, '%Y%m/%d %H:%M'))
        hum.append(tr.find('td', {'headers': 'hum'}).text)
        rain.append(tr.find('td', {'headers': 'rain'}).text)
        sunlight.append(tr.find('td', {'headers': 'sunlight'}).text)
        temp.append(tr.find('td', {'headers': 'temp'}).text)
        visible.append(tr.find('td', {'headers': 'visible-1'}).text)
        weather.append(tr.find('td', {'headers': 'weather'}).find('img')['title'])
        wind_direction.append(tr.find('td', {'headers': 'w-1'}).text)
        wind_speed.append(tr.find('td', {'headers': 'w-2'}).text)
        break
    driver.quit()


while True:
    try:
        if allDead:
            break

        do_read()

        print('date:', date[-1])
        print('temp:', temp[-1])
        print('hum:', hum[-1])
        print('rain:', rain[-1])
        print('sunlight:', sunlight[-1])
        print('visible:', visible[-1])
        print('weather:', weather[-1])
        print('wind_direction:', wind_direction[-1])
        print('wind_speed:', wind_speed[-1])

        DAN.push('date', f'date:{date[-1]}')
        time.sleep(0.5)
        DAN.push('temp', f'temp:{temp[-1]}')
        time.sleep(0.5)
        DAN.push('hum', f'hum:{hum[-1]}')
        time.sleep(0.5)
        DAN.push('rain', f'rain:{rain[-1]}')
        time.sleep(0.5)
        DAN.push('sunlight', f'sunlight:{sunlight[-1]}')
        time.sleep(0.5)
        DAN.push('visible', f'visible:{visible[-1]}')
        time.sleep(0.5)
        DAN.push('weather', f'weather:{weather[-1]}')
        time.sleep(0.5)
        DAN.push('wind_direction', f'wind_direction:{wind_direction[-1]}')
        time.sleep(0.5)
        DAN.push('wind_speed', f'wind_speed:{wind_speed[-1]}')
        time.sleep(0.5)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    try:
        time.sleep(0.2)
    except KeyboardInterrupt:
        break

time.sleep(0.25)
try:
    DAN.deregister()  # 試著解除註冊
except Exception as e:
    print("===")
print("Bye ! --------------", flush=True)
sys.exit()
