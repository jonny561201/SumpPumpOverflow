import time


def test_something():
    # stopFlag = Event()
    # thread = MyThread(stopFlag, test_function, 4)
    # thread.start()

    print('my thread')
    time.sleep(1)

    # this will stop the timer
    # stopFlag.set()


def test_function():
    print('-----my test thread-----')
