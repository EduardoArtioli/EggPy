import numpy as np
import pyautogui
from pynput.keyboard import *
from PIL import ImageGrab

#  ======== settings ========
delay = 2  # in seconds
click_hold = 3  # in seconds
resume_key = Key.f1
pause_key = Key.f2
exit_key = Key.esc
#  ==========================

pause = True
running = True

def on_press(key):
    global running, pause

    if key == resume_key:
        pause = False
        print("[Resumed]")
    elif key == pause_key:
        pause = True
        print("[Paused]")
    elif key == exit_key:
        running = False
        print("[Exit]")


def display_controls():
    print("// AutoClicker by iSayChris")
    print("// - Settings: ")
    print("\t delay = " + str(delay) + ' sec' + '\n')
    print("// - Controls:")
    print("\t F1 = Resume")
    print("\t F2 = Pause")
    print("\t F3 = Exit")
    print("-----------------------------------------------------")
    print('Press F1 to start ...')

# def get_drone_position():
    # screenshot = pyautogui.locateOnScreen('assets/drone/1.png', confidence=0.9, region=(1021, 200, 1412, 688))

    # if screenshot:
    #     print(screenshot)
    #     return pyautogui.center(screenshot)
    # else:
    #     return None

def main():
    lis = Listener(on_press=on_press)
    lis.start()

    display_controls()

    # while True:
    #     img = ImageGrab.grab(bbox=(1000, 155, 1450, 750))
    #     img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    #     lower_thresh = np.array([0], dtype = "uint8")
    #     upper_thresh = np.array([100], dtype = "uint8")

    #     mask = cv2.inRange(img, lower_thresh, upper_thresh)


    #     detected_output = cv2.bitwise_and(img, img, mask = mask)
    #     cv2.imshow("red color detection", detected_output)
    #     # cv2.waitKey(0)




    #     if (cv2.waitKey(1) & 0xFF) == ord('q'):
    #         cv2.destroyAllWindows()
    #         break



    while running:

        # screenshot = ImageGrab.grab(bbox=(1021, 200, 1412, 688))
        # # screenshot = ImageGrab.grab(bounding_box)
        # cv2.imshow('screen', np.array(screenshot))

        if not pause:
            pyautogui.mouseDown(pyautogui.position())
            pyautogui.PAUSE = click_hold
            pyautogui.mouseUp(pyautogui.position())
            pyautogui.PAUSE = delay

            print(pyautogui.position())

            # get_drone_position()
            # pyautogui.click(get_drone_position())
            # pyautogui.PAUSE = 0.1

    lis.stop()


if __name__ == "__main__":
    main()