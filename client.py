import recogniser.face_recogniser as camera
import screenshot.screenshoter as screen
import dawn_mode as listener
from active_proc import *
import datetime
import threading
import time
import requests

#get_active_window()
active_hist = []
photo = camera.make_photo()
screenshot = screen.get_screen_shot()
clicks = []

def active_progs():
    global active_hist
    prev_active = get_active_window()
    start = datetime.datetime.now()
    while True:
        active_window = get_active_window()
        if prev_active != active_window:
            finish = datetime.datetime.now()
            for i in active_hist:
                if prev_active == i['proc']:
                    delta = finish - start
                    i['time'] += float(delta.seconds) / 60.0
                    break
            else:
                prev_active.append({"proc": prev_active, "time": float((finish - start).seconds) / 60.0})
            start = finish
            prev_active = active_window
        time.sleep(5)


def clicker():
    #если кликов нет 20 минут, то делаем скриншот и камеру
    global clicks
    while True:
        listener.start()
        time.sleep(30)
        clicks = listener.stop()


def get_photo():
    user_photo = camera.make_photo()
    return user_photo


def main():
    global active_hist, photo, screenshot, clicks
    with open('start.txt', 'r') as file:
        name, surname = file.readline().split()
        start_photo = get_photo()
        requests.post("http://localhost:5050/addUser", data={"name": name, "surname": surname, "photo": start_photo})
    time.slip(300)
    while True:
        photo = camera.make_photo()
        screenshot = screen.get_screen_shot()
        requests.post("http://localhost:5050/addInfo", data={"surname": surname,
                                                             "date": datetime.datetime.now(),
                                                             "active_hist": active_hist,
                                                             "photos": photo,
                                                             "screenshots": screenshot,
                                                             "clicks": clicks})
        time.sleep(30)



#30 seconds => add_info("")

#1thread clicker 2thread active 3thread main thread
#main thread start: request(localhost://addUser data={name,surname,photo})
#add info(data: datetime, active_history[{proc:name, tim},{}],[,photo],[massiv] : [screencast])