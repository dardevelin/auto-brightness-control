# we use ACPI to figure out the max brightness level supported as
# well as the current brightness value
# we just assume this always work, if it doesn't the program will not work at all
# let it crash

import os
import Helper
import BrightnessMode as BMode

class SystemBrightness(object):
    def __init__(self, path='/sys/class/backlight/acpi_video0'):
        # this function supports custom paths were a max_brightness and a
        # actual_brightness file may be present to define the card limits
        self.current = None
        self.max = None
        current_path = "{}/actual_brightness".format(path)
        max_path = "{}/max_brightness".format(path)

        with open(max_path, 'r') as f:
             self.max = int(f.read())

        with open(current_path, 'r') as f:
            self.current = int(f.read())



    def max_brightness(self, mode=BMode.BrightnessMode.RAW):
        if mode:
            return self.max

        return 100

    def current_brightness(self, mode=BMode.BrightnessMode.RAW):
        if mode:
            return self.current

        return Helper.calculate_percentile(self.current, min_range=1, max_range=self.max)

    def set_brightness(self, level, mode=BMode.BrightnessMode.PERCENTILE):
        if BMode.BrightnessMode.RAW == mode:
            level = Helper.calculate_percentile(level, min_range=1, max_range=100)

        os.system('xbacklight -set {}'.format(level))
