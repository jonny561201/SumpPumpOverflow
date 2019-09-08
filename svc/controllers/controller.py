from svc.utilities.gpio import get_intervals
from svc.utilities.depth import get_depth_by_intervals


# TODO: Need to make api call to save current depth
def measure_depth():
    start, stop = get_intervals()
    depth = get_depth_by_intervals(start, stop)
    return depth
