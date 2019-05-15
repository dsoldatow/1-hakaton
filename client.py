import recogniser.face_recogniser as camera
import screenshot.screenshoter as screen
import dawn_mode as listener
from active_proc import *
import datetime
from threading import Thread
import time
import requests
import predObr
import json
from base64 import b64encode

# get_active_window()
active_hist = []
photo = camera.make_photo()
screenshot = screen.get_screen_shot()
clicks = {}


def active_progs():
    global active_hist
    prev_active = get_active_window()
    start = datetime.datetime.now()
    while True:
        active_window = get_active_window()
        if active_window not in predObr.all_progs:
            time.sleep(5)
            continue
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
        requests.post("http://localhost:5050/add_user", data=json.dumps({"name": name, "surname": surname, "photo": b64encode(start_photo).decode()}))
    time.sleep(10)
    while True:
        photo = camera.make_photo()
        screenshot = screen.get_screen_shot()
        requests.post("http://localhost:5050/addInfo", data=json.dumps({"surname": surname,
                                                                       "date": str(datetime.datetime.now()),
                                                                       "active_hist": active_hist,
                                                                       "photo": b64encode(photo).decode(),
                                                                       "screenshot": screenshot,
                                                                       "clicks": clicks}))
        time.sleep(30)


if __name__ == "__main__":
    main_thread = Thread(target=main)
    active_thread = Thread(target=active_progs)
    clicker_thread = Thread(target=clicker)

    main_thread.start()
    active_thread.start()
    clicker_thread.start()
    main_thread.join()
    active_thread.join()
    clicker_thread.join()