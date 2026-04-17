import random
import time

from svc.utilities.depth import SPEED_OF_SOUND

MIN_DEPTH_CM = 30.0
MAX_DEPTH_CM = 40.0


def get_intervals():
    depth = random.uniform(MIN_DEPTH_CM, MAX_DEPTH_CM)
    interval = (depth * 2) / SPEED_OF_SOUND

    start = time.time()
    stop = start + interval
    return start, stop
