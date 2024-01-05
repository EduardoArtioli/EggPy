
from pynput.keyboard import *
import numpy as np
# Constants
RESUME_KEY = Key.f1
PAUSE_KEY = Key.f2
EXIT_KEY = Key.esc
DELAY = 2 
CLICK_HOLD = 4
DRONE_CLICK_DELAY = 2
CHECK_WINDOW_OPENING_DELAY = 1.5

X_OFFSET = 921
Y_OFFSET = 66
SCREENSHOT_WIDTH = 591
SCREENSHOT_HEIGHT = 788

# OPTIMIZED = False
# X_OFFSET = 921 + 145
# Y_OFFSET = 66 + 90
# SCREENSHOT_WIDTH = 591 - 145 - 60
# SCREENSHOT_HEIGHT = 788 - 90 - (788 - 676)

# Ignore areas are defined as ( x_start, y_start, x_end, y_end )
IGNORE_AREAS = {
    'top': (0, 0, SCREENSHOT_WIDTH, 90),
    'left': (0, 90, 145, 450),
    'bottom': (0, 676, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT),
    'right': (SCREENSHOT_WIDTH - 60, 90, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT - (SCREENSHOT_HEIGHT - 676)),
    'bottomButton': (325, 665, 375, 676),
}
THRESHOLD_LOW = np.array([0], dtype="uint8")
THRESHOLD_HIGH = np.array([100], dtype="uint8")

WINDOWS_SIZES = {
    'HEN HOUSING': { 'width': 431, 'height': 529 },
    'GRAIN SILOS': { 'width': 437, 'height': 426 },
    'RESEARCH CENTER': { 'width': 460, 'height': 582 },
    'SHIPPING DEPOT': { 'width': 436, 'height': 561 },
    'RANDOM GIFT': { 'width': 235, 'height': 240 },
    'MULTIPLAYER': { 'width': 230, 'height': 151 },
    'RUNNING CHICKEN': { 'width': 230, 'height': 178 },
    'VEICHLE EVENT': { 'width': 158, 'height': 188 },
    'DRONE EVENT ULTRA': { 'width': 231, 'height': 297 },
    'MISSION CONTROL': { 'width': 452, 'height': 361 },
}
