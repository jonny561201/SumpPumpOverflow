from svc.config.settings_state import Settings


def create_gpio():
    environment = Settings.get_instance().environment
    if environment == 'prod':
        from svc.utilities.gpio import get_intervals
    else:
        from svc.utilities.gpio_stub import get_intervals
    return get_intervals
