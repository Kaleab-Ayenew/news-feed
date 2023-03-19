from poster import main_task
import time

mins = 1


def deamon():
    while True:
        main_task()
        time.sleep(60*mins)


deamon()
