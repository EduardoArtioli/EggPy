import cv2
import numpy as np
import pyautogui
from pynput.keyboard import *
from PIL import Image
import Quartz.CoreGraphics as CG
import time
from macos_image import capture_screenshot

# Constants
RESUME_KEY = Key.f1
PAUSE_KEY = Key.f2
EXIT_KEY = Key.esc
DELAY = 2 
CLICK_HOLD = 3 
X_OFFSET = 1000
Y_OFFSET = 155
SCREENSHOT_WIDTH = 500
SCREENSHOT_HEIGHT = 580
# Ignore areas are defined as ( x_start, y_start, x_end, y_end )
IGNORE_AREAS = {
    'events': (0, 55, 50, 200),
    'packages': (0, 450, 120, 580),
    'messages': (450, 0, 500, 300)
}
THRESHOLD_LOW = np.array([0], dtype="uint8")
THRESHOLD_HIGH = np.array([100], dtype="uint8")

WINDOWS_SIZES = {
    'HEN HOUSING': { 'width': 440, 'height': 529 },
    'GRAIN SILOS': { 'width': 440, 'height': 401 },
    'RESEARCH CENTER': { 'width': 447, 'height': 573 },
    'SHIPPING DEPOT': { 'width': 440, 'height': 561 },
    'RANDOM GIFT': { 'width': 235, 'height': 240 },
    'MULTIPLAYER': { 'width': 230, 'height': 151 },
}

# Global variables
clicked = False
pause = True
running = True

def on_press(key):
    global running, pause
    if key == RESUME_KEY:
        pause = False
        print("[Resumed]")
    elif key == PAUSE_KEY:
        pause = True
        print("[Paused]")
    elif key == EXIT_KEY:
        running = False
        print("[Exit]")

def apply_ignore_areas(img):
    for area in IGNORE_AREAS.values():
        img[area[1]:area[3], area[0]:area[2]] = 255
    return img

def process_image(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img = apply_ignore_areas(img)
    mask = cv2.inRange(img, THRESHOLD_LOW, THRESHOLD_HIGH)
    return Image.fromarray(mask), img

def draw_ignored_areas(img):
    for area in IGNORE_AREAS.values():
        img = cv2.rectangle(img, (area[0], area[1]), (area[2], area[3]), (0, 0, 255), 2)
    return img

def process_image(img):
    img_grey = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    # apply ignore areas to grey image
    img_grey = apply_ignore_areas(img_grey)
    img_masked = cv2.inRange(img_grey, THRESHOLD_LOW, THRESHOLD_HIGH)
    return Image.fromarray(img_masked), img_grey

def draw_debug_image(img):
    img = draw_ignored_areas(img)
    cv2.imshow("Drone Catcher", img)

def image_processing(debug = False):
    img_rgb = capture_screenshot(X_OFFSET, Y_OFFSET, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT);
    img_masked, img_grey = process_image(img_rgb)
    bbox = img_masked.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        print(f"BBox Size: Width = {bbox_width}, Height = {bbox_height}")

        # if the bbox width and height is bigger than 300, then it's probably a window
        if bbox_width > 300 and bbox_height > 300:
            window_name = None
            for window in WINDOWS_SIZES:
                if bbox_width == WINDOWS_SIZES[window]['width'] and bbox_height == WINDOWS_SIZES[window]['height']:
                    window_name = window
                    break
            if window_name is not None:
                print(f"Found {window_name} window")
                click_on_window(window_name)
                return None, None


        if bbox_width > 300 and bbox_height > 300:
            draw_debug_image(img_rgb)
            return 0, 0
        x = int((x1 + x2) / 2) + X_OFFSET
        y = int((y1 + y2) / 2) + Y_OFFSET
        if debug:
            img_rgb = cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
            draw_debug_image(img_rgb)
        return x, y
    else:
        if debug:
            draw_debug_image(img_rgb)
        return None, None
    

DRONE_CLICK_DELAY = 2
clicked_time = 0
def click_on_drone( x, y, drag = True ):
    global clicked, pause, clicked_time
    if not pause:
        print("Clicking on drone at: ", x, y)
        pyautogui.mouseDown( x = x, y = y, button = 'left' )
        if drag:
            pyautogui.mouseUp( x = x + 5, y = y + 5, button = 'left', duration = 0.3 )
        else:
            pyautogui.mouseUp( x = x, y = y, button = 'left', duration = 0.1 )
        pyautogui.moveTo(1200, 800);
        clicked = True
        clicked_time = time.time()

def click_on_window( window_name ):
    global clicked, pause, clicked_time
    x = 0
    y = 0
    if not pause:
        match window_name:
            case 'HEN HOUSING':
                x = 1420
                y = 189
            case 'GRAIN SILOS':
                x = 1420
                y = 254
            case 'RESEARCH CENTER':
                x = 1420
                y = 189
            case 'SHIPPING DEPOT':
                x = 1420
                y = 189
            case 'RANDOM GIFT':
                x = 1215
                y = 548
            case 'MULTIPLAYER':
                x = 1215
                y = 548
            case _:
                print("Window not found")
                return
        print("Clicking on window: ", window_name)
        pyautogui.click( x = x, y = y, button = 'left' )
        pyautogui.moveTo(1200, 800);
        clicked = True
        clicked_time = time.time()


def drone_catcher():
    global clicked_time

    current_time = time.time()

    x, y = image_processing(debug = True)

    if x is not None and y is not None:
        if x > 0 and y > 0:
            if (current_time - clicked_time >= DRONE_CLICK_DELAY):
                click_on_drone( x, y, True )


mouse_released_time = 0
mouse_pressed = False
mouse_press_time = 0
def hatch_chickens():
    global mouse_released_time, mouse_pressed, mouse_press_time, pause
    current_time = time.time()
    if not pause:
        if not mouse_pressed and (current_time - mouse_released_time >= DELAY):
            pyautogui.mouseDown(pyautogui.position())
            mouse_pressed = True
            mouse_press_time = time.time()

        # Handle mouse actions
        if mouse_pressed and (current_time - mouse_press_time >= CLICK_HOLD):
            pyautogui.mouseUp(pyautogui.position())
            mouse_pressed = False
            mouse_released_time = current_time


loop_time = time.time()
def main():
    global loop_time

    lis = Listener(on_press=on_press)
    lis.start()

    while True:
        drone_catcher()
        hatch_chickens()

        time.sleep(0.02)

        # print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

    lis.stop()

if __name__ == "__main__":
    main()