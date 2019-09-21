from threading import Thread, Event


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            print("my thread")
            # call a function


stopFlag = Event()
try:
    thread = MyThread(stopFlag)
    thread.start()
except KeyboardInterrupt:
    stopFlag.set()
# this will stop the timer
