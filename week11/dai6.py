import DAN
import random
import sys
import threading
import time
from tkinter import *

ServerURL = 'https://3.iottalk.tw'
myName = "DEN." + str(random.randint(600, 999))

tk = Tk()
tk.title("DEN Tk_Slider")
text_widget = Text(tk, height=2, width=36, font=("Simsun", 24), fg="red", bg="lightgreen")
text_widget.pack()
text_widget.insert(END, "拉到滿意的值然後放掉滑鼠!")

gotSlider = False
sliderVal = 58
firstSetSlider = True


def syy_changed(event):
    global gotSlider, sliderVal
    sliderVal = s.get()
    gotSlider = True


s = Scale(tk, from_=0, to=100, length=600, tickinterval=10, bg="lightyellow", fg="red",
          orient=HORIZONTAL)
s.bind("<ButtonRelease-1>", syy_changed)
s.set(sliderVal)
s.pack()


def kill_me():
    global allDead  # 用來通知 thread 自殺
    allDead = True  # 通知所有 thread 自殺
    tk.focus_set()
    sayBye()
    tk.quit()  # close Tk window


button = Button(tk, text="Quit 點這結束程式", anchor="w",
                bg="yellow", fg="green", command=kill_me)
button.pack(side='right')
tk.protocol("WM_DELETE_WINDOW", kill_me)

Reg_addr = None

DAN.profile['dm_name'] = 'DEN_Dummy_253'
DAN.profile['df_list'] = ['Slider', 'Color-I', 'Dmy_d253', 'Dummy_Control']


def initIoTtalk():
    DAN.profile['d_name'] = myName + "_" + DAN.profile['dm_name']  # None
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    print("dm_name is ", DAN.profile['dm_name'])
    print("Server is ", ServerURL)


##
theInput = "haha"
gotInput = allDead = False
firstRead = True


def doRead():
    global gotInput, theInput, allDead, firstRead
    while True:
        if (allDead): break
        if gotInput:
            time.sleep(0.1)
            continue  # go back to while
        try:
            if firstRead:
                print("提醒輸入 quit 會結束 !")  # 只在第一次輸入之前才提醒
                firstRead = False
            theInput = input("Give me data: ")

            tokens = theInput.split(' ')
            if tokens[0] == 'L' and len(tokens) == 2:
                DAN.push("Slider", min(max(int(tokens[1]), 0), 99))
            elif tokens[0] == 'C' and len(tokens) == 4:
                restrict_input = [0, 0, 0]
                for i in range(1, 4):
                    restrict_input[i - 1] = min(max(int(tokens[i]), 0), 255)
                DAN.push("Color-I", restrict_input[0], restrict_input[1], restrict_input[2])
            else:
                print("輸入格式錯誤, 請重新輸入 !")
        except KeyboardInterrupt:
            allDead = True
            break
        except Exception:  ##  KeyboardInterrupt:
            allDead = True
            sys.stdout = sys.__stdout__
            print(" Thread say Bye bye ---------------", flush=True)
            break  # raise   #  sys.exit(0);   ## break  # raise   #  ?
        gotInput = True
        if (allDead):
            kill_me()
        elif theInput != 'quit' and theInput != "exit":
            print("Will send " + theInput, end="   , ")


# creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw
threadx = threading.Thread(target=doRead)
threadx.daemon = True


def doDummy():  # 因為 Tkinter  必須在 main thread, 所以原先的主程式必須改用 thread (thready)
    global gotInput, theInput, allDead  # do NOT forget these var should be global
    global gotSlider, firstSetSlider  # 沒寫  sliderVal = xxx 就不必寫 global
    while True:
        if (allDead): break
        try:
            # Pull data from a device feature called "Dummy_Control"
            value1 = DAN.pull('Dummy_Control')
            if value1 != None:
                print(value1[0])
            # Push data to a device feature called "Dummy_Sensor"
            if gotSlider:  # Slider 有被動到
                sss = sliderVal  # 取出 slider value
                gotSlider = False  # 其實沒用處, 因為我們不管 user 是否會去改變  Slider
                DAN.push('Slider', sss)

            # end of if gotSlider
            if gotInput:
                if theInput == 'quit' or theInput == "exit":
                    allDead = True
                    break;  # sys.exit( );
                # value2=random.uniform(1, 10)
                try:
                    value2 = float(theInput)
                except:
                    value2 = 0
                gotInput = False  # so that you can input again
                if (allDead): break;
                DAN.push('Dummy_Control', value2, value2)  # 故意多送一個
            # end of if gotInput
        except KeyboardInterrupt:
            allDead = True
            break;  # sys.exit( );
        except Exception as e:
            print("allDead: ", allDead)
            if (allDead):
                break  # do NOT try to re-register !
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr IS not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)
        if (allDead): break
        try:
            time.sleep(0.1)  # was 0.2
        except KeyboardInterrupt:
            break
    print("=== end of thready")
    time.sleep(0.015)
    kill_me();
    sys.exit(0);


def sayBye():  # 用來向 IoTtalk 解除註冊 Deregister
    try:
        time.sleep(0.025)
        DAN.deregister()
    except Exception as e:
        print("===De-Reg Error")
    print("Bye ! --------------", flush=True)
    # sys.exit(0);


# 以下三列把 doDummy 包成 thready 然後叫它平行啟動
thready = threading.Thread(target=doDummy)
thready.daemon = True

if __name__ == '__main__':
    initIoTtalk()
    threadx.start()
    thready.start()
    tk.mainloop()  # tk GUI 必須當老大, 在 main thread
