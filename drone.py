import cv2
from pynput.keyboard import *
import time
from macos_image import capture_screenshot
from mouse import *
from defines import *
from image_processing import *

# Global variables
pause = True
running = True
clicked_time = 0
hits_count = 0
stop_hatching = False
check_window_time = None
mouse_released_time = 0
mouse_pressed = False
mouse_press_time = 0
stopped_hatching = False

def image_processing(debug = False):
    global check_window_time, stop_hatching
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
        if bbox_width >= 230 and bbox_height >= 151:
            if not check_window_time:
                check_window_time = time.time()
                return None, None
            else:
                if time.time() - check_window_time >= CHECK_WINDOW_OPENING_DELAY:
                    check_window_time = None
                    print("2 seconds have passed, processing window...")
                    window_name = None
                    for window in WINDOWS_SIZES:
                        target_width = WINDOWS_SIZES[window]['width']
                        target_height = WINDOWS_SIZES[window]['height']
                        if (target_width - 10 <= bbox_width <= target_width + 10) and \
                        (target_height - 10 <= bbox_height <= target_height + 10):
                            window_name = window
                            stop_hatching = True
                            break
                    if window_name is not None:
                        print(f"Found {window_name} window")
                        click_on_window(window_name)
                        return None, None
                return None, None
        else:
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

def click_on_drone( x, y):
    global pause, clicked_time, hits_count, stop_hatching
    if not pause:
        mouseClick(x, y)
        hits_count += 1
        print(f"Hits: {hits_count}")
        clicked_time = time.time()
        mouseMove(X_OFFSET + SCREENSHOT_WIDTH / 2, 800)

def click_on_window(window_name):
    global pause, clicked_time
    window_coordinates = {
        'HEN HOUSING': (1420, 188),
        'GRAIN SILOS': (1420, 254),
        'RESEARCH CENTER': (1430, 175),
        'SHIPPING DEPOT': (1420, 188),
        'RANDOM GIFT': (1200, 550),
        'MAIN MENU': (1420, 268),
        'MULTIPLAYER': (1200, 500),
        'RUNNING CHICKEN': (1200, 550),
        'VEICHLE EVENT': (1200, 550),
        'DRONE EVENT ULTRA': (1210, 570),
        'MISSION CONTROL': (1420, 270)
    }
    if pause:
        return
    coordinates = window_coordinates.get(window_name)
    if coordinates:
        print(f"Clicking on window: {window_name}")
        mouseMove(*coordinates)
        time.sleep(0.5)
        mouseClick(*coordinates)  # Unpacks the tuple into x and y
        clicked_time = time.time()
        print(f"Clicked on {window_name}")
        mouseMove(X_OFFSET + SCREENSHOT_WIDTH / 2, 800)  # Move mouse to a default position
    else:
        print("Window not found")

def drone_catcher():
    global clicked_time, stop_hatching
    current_time = time.time()
    x, y = image_processing(debug = True)
    if x is not None and y is not None:
        if x > 0 and y > 0:
            stop_hatching = True
            if (current_time - clicked_time >= DRONE_CLICK_DELAY):
                click_on_drone( x, y )

def hatch_chickens():
    global mouse_released_time, mouse_pressed, mouse_press_time, pause, stop_hatching, stopped_hatching
    current_time = time.time()
    if not pause:
        if not mouse_pressed and (current_time - mouse_released_time >= DELAY):
            mouse_pos = mousePosition()
            if mouse_pos[1] != 800:
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

def on_press(key):
    global running, pause
    if key == RESUME_KEY:
        pause = False
        mouseMove(X_OFFSET + SCREENSHOT_WIDTH / 2, 800)
        print("[Resumed]")
    elif key == PAUSE_KEY:
        pause = True
        print("[Paused]")
    elif key == EXIT_KEY:
        running = False
        print("[Exit]")

# loop_time = time.time()
def main():
    # global loop_time
    lis = Listener(on_press=on_press)
    lis.start()
    while True:
        drone_catcher()
        hatch_chickens()
        # time.sleep(0.01)
        # print('FPS {}'.format(1 / (time.time() - loop_time)))
        # loop_time = time.time()
        if (cv2.waitKey(1) & 0xFF) == ord('q') or not running:
            cv2.destroyAllWindows()
            break
    lis.stop()

if __name__ == "__main__":
    main()