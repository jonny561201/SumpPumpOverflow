from time import sleep

from svc.controllers.controller import measure_depth

try:
    while True:
        depth = measure_depth()
        print('Depth measure: ' + str(depth) + 'cm')
        sleep(120)
except KeyboardInterrupt:
    print('Application interrupted by user')
