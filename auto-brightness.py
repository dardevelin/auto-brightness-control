#!/usr/bin/env python

import sys
import cv2
from PIL import Image

import ABConfig
import Brightness
import BrightnessMode as BMode
import SystemBrightness as Sb

CFG = ABConfig.Config()
# we use opencv to control the camera and to take a picture
# usually the default device is number as 0, so we set it here
DEVICEID=int(CFG.get('CameraDeviceID', 0))

camera = cv2.VideoCapture(DEVICEID)

# take our picture
rectangle, frame = camera.read()

# if we didn't get a rectangle something went wrong abort
if not rectangle:
    sys.exit()

# convert our opencv image to PIL image
picture = Image.fromarray( cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) )

# look at one pixel to evalute the brightness level
X, Y = 0, 0

pixel = picture.getpixel((X,Y))
# we need RGB individual values to apply the brightness formula
R,G,B = pixel

# we average the result of 3 different ways of calculating the brightness
outside_b = Brightness.BrightnessCalculator(R,G,B).average(
    BMode.BrightnessMode.PERCENTILE)

system_ctrl = Sb.SystemBrightness(CFG.get('SystemBrightnessPath'))
monitor_b = system_ctrl.current_brightness(mode=BMode.BrightnessMode.PERCENTILE)

# the user doesn't want to be bellow this level
auto_min_b = int(CFG.get('AutoMinBrightness'))
# the user doesn't want to be above this level
auto_max_b = int(CFG.get('AutoMaxBrightness'))

auto_add_mode = int(CFG.get('AutoAddMode'))

# set default change level to be current brightness level
brightness = monitor_b

if not auto_add_mode:
    if outside_b < auto_min_b:
        brightness = auto_min_b
    elif outside_b > auto_max_b:
        brightness = auto_max_b
else: # add mode on
    if auto_min_b + outside_b <= auto_max_b:
        brightness = auto_min_b + outside_b
    else:
        brightness = auto_max_b

system_ctrl.set_brightness(brightness)
