from svc.utilities.gpio import get_intervals
from svc.utilities.depth import get_depth_by_intervals
from svc.utilities.api_requests import save_current_daily_depth

USER_ID = None
# TODO: Need to make api call to save current depth
# TODO: Make into class to keep a running average of current depth
def measure_depth():
    start, stop = get_intervals()
    depth = get_depth_by_intervals(start, stop)
    save_current_daily_depth(USER_ID, depth, stop)
    return depth
