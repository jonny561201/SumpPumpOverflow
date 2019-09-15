from time import sleep

from svc.controllers.controller import DepthController

try:
    while True:
        controller = DepthController()
        depth = controller.measure_depth()
        print('Depth measure: ' + str(depth) + 'cm')
        sleep(120)
except KeyboardInterrupt:
    print('Application interrupted by user')
