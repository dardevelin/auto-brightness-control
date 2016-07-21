# in here we handle configuraiton loading
import os
import csv

class Config:
    def __init__(self, path='.config/auto-brightness-control'):
        self.home = os.environ['HOME']
        path = "{}/{}".format(self.home,path)
        self.configs = {}

        self.file_path = path + '/abc.cfg'
        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(self.file_path):
            self.create_default_config()

        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            self.configs = dict(reader)

    def get(self, key, default_value=None):
        return self.configs.get(key, default_value)

    def create_default_config(self):
        default_cfg = {
            'CameraDeviceID':'0',
            'SystemBrightnessPath':'/sys/class/backlight/acpi_video0',
            'AutoMinBrightness':'30',
            'AutoMaxBrightness':'100',
            'AutoAddMode':'1' # 0 for false, everything else for true
        }

        with open(self.file_path, 'w+') as f:
            writer = csv.writer(f)
            for key, value in default_cfg.items():
                writer.writerow([key,value])
