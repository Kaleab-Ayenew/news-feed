from main import run
import time

mins = 1


def deamon():
    while True:
        run()
        time.sleep(60*mins)


deamon()
