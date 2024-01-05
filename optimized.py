import cv2
from PIL import Image
from pynput.keyboard import *
import time
import numpy as np
from macos_image import capture_screenshot
from mouse import *

# Constants
RESUME_KEY = Key.f1
PAUSE_KEY = Key.f2
EXIT_KEY = Key.esc
DELAY = 2 
CLICK_HOLD = 4

# X_OFFSET = 921
# Y_OFFSET = 66
# SCREENSHOT_WIDTH = 591
# SCREENSHOT_HEIGHT = 788

# OPTIMIZED = False
X_OFFSET = 921 + 145
Y_OFFSET = 66 + 90
SCREENSHOT_WIDTH = 591 - 145 - 60
SCREENSHOT_HEIGHT = 788 - 90 - (788 - 676)

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

# Global variables
pause = True
running = True

def on_press(key):
    global running, pause
    if key == RESUME_KEY:
        pause = False
        mouseMove(1200, 800)
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

def draw_ignored_areas(img):
    for area in IGNORE_AREAS.values():
        img = cv2.rectangle(img, (area[0], area[1]), (area[2], area[3]), (0, 0, 255), 2)
    return img

def process_image(img):
    img_grey = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    # img_grey = apply_ignore_areas(img_grey)
    img_masked = cv2.inRange(img_grey, THRESHOLD_LOW, THRESHOLD_HIGH)
    return Image.fromarray(img_masked)

def draw_debug_image(img):
    img = draw_ignored_areas(img)
    cv2.imshow("Drone Catcher", img)

check_window_time = None
def image_processing(debug = False):
    global check_window_time
    img_rgb = capture_screenshot(X_OFFSET, Y_OFFSET, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT);
    img_masked = process_image(img_rgb)
    bbox = img_masked.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        # print(f"BBox Size: Width = {bbox_width}, Height = {bbox_height}")

        img_rgb = cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        draw_debug_image(img_rgb)
        # if the bbox width and height is bigger than 300, then it's probably a window
        if bbox_width >= 230 and bbox_height >= 151:
            if not check_window_time:
                # Window detected, start the timer
                check_window_time = time.time()
                return None, None
            else:
                # Check if 2 seconds have passed
                if time.time() - check_window_time >= 1.5:
                    # 2 seconds have passed, reset the timer and do the task
                    check_window_time = None
                    # Your logic after 2 seconds
                    print("2 seconds have passed, processing window...")
                    window_name = None
                    for window in WINDOWS_SIZES:
                        target_width = WINDOWS_SIZES[window]['width']
                        target_height = WINDOWS_SIZES[window]['height']
                        
                        if (target_width - 10 <= bbox_width <= target_width + 10) and \
                        (target_height - 10 <= bbox_height <= target_height + 10):
                            window_name = window
                            break
                    if window_name is not None:
                        print(f"Found {window_name} window")
                        click_on_window(window_name)
                        return None, None
                return None, None
        else:
            # Reset the timer
            check_window_time = None

        if bbox_width > 300 and bbox_height > 300:
            return 0, 0
        x = int((x1 + x2) / 2) + X_OFFSET
        y = int((y1 + y2) / 2) + Y_OFFSET
        return x, y
    else:
        if debug:
            draw_debug_image(img_rgb)
        return None, None
    

DRONE_CLICK_DELAY = 2
clicked_time = 0

hits_count = 0
stop_hatching = False

def click_on_drone( x, y):
    global pause, clicked_time, hits_count, stop_hatching
    if not pause:
        mouseClick(x, y)
        hits_count += 1
        print(f"Hits: {hits_count}")
        clicked_time = time.time()
        mouseMove(1200, 800)

def click_on_window( window_name ):
    global pause, clicked_time
    x = 0
    y = 0
    if not pause:
        # if  mouseIsDown():
        #     print("Mouse is down, releasing...")
        #     mouseUp()
        match window_name:
            case 'HEN HOUSING':
                x = 1420
                y = 188
            case 'GRAIN SILOS':
                x = 1420
                y = 254
            case 'RESEARCH CENTER':
                x = 1430
                y = 175
            case 'SHIPPING DEPOT':
                x = 1420
                y = 188
            case 'RANDOM GIFT':
                x = 1200
                y = 550
            case 'MULTIPLAYER':
                x = 1200
                y = 500
            case 'RUNNING CHICKEN':
                x = 1200
                y = 550
            case 'VEICHLE EVENT':
                x = 1200
                y = 550
            case 'DRONE EVENT ULTRA':
                x = 1210
                y = 570
            case 'MISSION CONTROL':
                x = 1420
                y = 270
            case _:
                print("Window not found")
                return
        print("Clicking on window: ", window_name)
        mouseClick(x, y)
        clicked_time = time.time()
        mouseMove(1200, 800)

def drone_catcher():
    global clicked_time, stop_hatching
    current_time = time.time()
    x, y = image_processing(debug = True)
    if x is not None and y is not None:
        if x > 0 and y > 0:
            stop_hatching = True
            if (current_time - clicked_time >= DRONE_CLICK_DELAY):
                click_on_drone( x, y )

mouse_released_time = 0
mouse_pressed = False
mouse_press_time = 0
stopped_hatching = False
def hatch_chickens():
    global mouse_released_time, mouse_pressed, mouse_press_time, pause, stop_hatching, stopped_hatching
    current_time = time.time()
    if not pause:
        if not mouse_pressed and (current_time - mouse_released_time >= DELAY):
            if(mousePosition() != (1200, 800)):
                return
            mouseDown()
            mouse_pressed = True
            mouse_press_time = time.time()
            stopped_hatching = False

        if mouse_pressed and (current_time - mouse_press_time >= CLICK_HOLD) or stop_hatching:
            if not stopped_hatching:
                mouseUp()
                mouse_pressed = False
                stop_hatching = False
                mouse_released_time = current_time
                stopped_hatching = True



loop_time = time.time()
def main():
    global loop_time

    lis = Listener(on_press=on_press)
    lis.start()

    while True:
        drone_catcher()
        hatch_chickens()

        time.sleep(0.01)
        # print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q') or not running:
            cv2.destroyAllWindows()
            break

    lis.stop()

if __name__ == "__main__":
    main()