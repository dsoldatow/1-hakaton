import recogniser.face_recogniser
import screenshot.screenshoter
import dawn_mode
from active_proc import *
import datetime
import threading
import time

#get_active_window()
time_hist = []
def active_progs():
    global time_hist
    prev_active = get_active_window()
    start = datetime.datetime.now()
    while True:
        active_window = get_active_window()
        if prev_active != active_window:
            finish = time.time()
            if prev_active in time_hist.keys():
                time_hist[prev_active] += finish - start
            else:
                time_hist[prev_active] = finish - start
            start = finish
            prev_active = active_window
        time.sleep(5)


def clicker():
    #если кликов нет 20 минут, то делаем скриншот и камеру
    pass


def get_photo():
    pass


#30 seconds => add_info("")

#1thread clicker 2thread active 3thread main thread
#main thread start: request(localhost://addUser data={name,surname,photo})
#add info(data: datetime, active_history[{time:123, proc:str},{}],[,photo],[massiv] : [screencast])