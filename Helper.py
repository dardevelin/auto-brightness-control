# This Class contains all our helper functions


def calculate_percentile(value, min_range=1, max_range=255):
    # 1 == 0%, 255 == 100%
    # max_range - 100%
    # value - x
    return value * 100 / max_range

def calculate_value(percentage, min_range=1, max_range=255):
    # 1 == 0%, 255 == 100%
    # max_range - 100%
    # x  - percentage
    return percentage * max_range / 100
