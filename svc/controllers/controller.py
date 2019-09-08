from svc.utilities.gpio import get_intervals
from svc.utilities.depth import get_depth_by_intervals


def measure_depth():
    start, stop = get_intervals()
    get_depth_by_intervals(start, stop)
