from threading import Event

from svc.services.event import MyThread


def test_something():
    stopFlag = Event()
    thread = MyThread(stopFlag)
    thread.start()
    # this will stop the timer
    stopFlag.set()
