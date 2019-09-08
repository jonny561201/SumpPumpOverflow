import time
# import RPi.GPIO as GPIO

INPUT_PIN = 7
OUTPUT_PIN = 8

# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(INPUT_PIN, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(OUTPUT_PIN, GPIO.OUT)


def get_intervals():
    # _emit_chirp()
    start = time.time()
    stop = time.time()

    # while GPIO.input(INPUT_PIN) == 0:
    #     start = time.time()
    #
    # while GPIO.input(INPUT_PIN) == 1:
    #     stop = time.time()
    return start, stop


# def _emit_chirp():
    # GPIO.output(OUTPUT_PIN, True)
    #
    # time.sleep(0.00001)
    # GPIO.output(OUTPUT_PIN, False)
