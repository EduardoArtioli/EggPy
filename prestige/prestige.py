import time
import keyboard
import pyautogui
import Quartz.CoreGraphics as CG

from pynput.mouse import Button, Controller
import time

mouse = Controller()
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import kCGMouseEventSubtype
import Quartz.CoreGraphics as CG

def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None, 
                    type, 
                    (posx,posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mouseMove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy);

def mouseClick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        #mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx,posy);
        mouseEvent(kCGEventLeftMouseUp, posx,posy);

def mousePosition():
        pos = CG.CGEventGetLocation(CG.CGEventCreate(None))
        return int(pos.x),int(pos.y)

def mouseIsDown():
        currentEvent = CG.CGEventCreate(None)
        return CG.CGEventGetIntegerValueField(currentEvent, kCGMouseEventSubtype) == kCGEventLeftMouseDown

def mouseDown():
        mouseEvent(kCGEventLeftMouseDown, mousePosition()[0], mousePosition()[1]);

def mouseUp():
        mouseEvent(kCGEventLeftMouseUp, mousePosition()[0], mousePosition()[1]);

def mouseDownPos(x, y):
        mouseEvent(kCGEventLeftMouseDown, x, y);


def click_at(x, y):
    mouse.position = (x, y)  # Move
    time.sleep(0.5)
    mouse.click(Button.left, 1)


def click_at_position(x, y):
    """
    Sends a left mouse click at (x, y) using CoreGraphics (Quartz).
    """
    # Mouse down
    event_down = CG.CGEventCreateMouseEvent(
        None,
        CG.kCGEventLeftMouseDown,
        (x, y),
        CG.kCGMouseButtonLeft
    )
    CG.CGEventPost(CG.kCGHIDEventTap, event_down)

    # Mouse up
    event_up = CG.CGEventCreateMouseEvent(
        None,
        CG.kCGEventLeftMouseUp,
        (x, y),
        CG.kCGMouseButtonLeft
    )
    CG.CGEventPost(CG.kCGHIDEventTap, event_up)

def perform_sequence():
    """
    1. Press Option key
    2. Click at two different coordinates (2-second delay between)
    3. Release Option key
    """

    print("Pressing Option (alt).")
    pyautogui.keyDown('alt')
    time.sleep(2)  # Wait 2 seconds

    print("Click #1 at (1380, 310).")

    # pyautogui.click(500, 500)
    mouseDownPos(1380, 310)
    # mouseMove(1480, 410)
    pyautogui.moveTo(1480, 410, duration=1);
    time.sleep(2)  # Wait 2 seconds

    # print("Click #2 at (1200, 500).")
    mouseDownPos(1200, 500)
    mouseMove(1300, 600)
    # pyautogui.click(700, 700)
    time.sleep(2)  # Wait 2 seconds
    mouseMove(1300, 600)
    time.sleep(1)  # Wait 2 seconds

    print("Releasing Option (alt).")
    pyautogui.keyUp('alt')
    time.sleep(2)  # Wait 2 seconds at the end of the sequence

def main():
    print("Press F6 to perform the multi-click Option sequence. Press F7 to exit.")
    
    while True:
        try:
            if keyboard.is_pressed('f6'):
                # To prevent triggering multiple times if the user holds the key,
                # we can wait until F6 is released before proceeding.
                print("F6 pressed. Executing sequence in 2 seconds...")
                time.sleep(2)
                
                perform_sequence()
                
                # Optional small sleep so we don't detect F6 press again immediately
                time.sleep(0.5)

            if keyboard.is_pressed('f7'):
                print("Exiting...")
                break


            if keyboard.is_pressed('f8'):
                print("Current pointer position: ", mouse.position)
                break


            time.sleep(0.05)  # Small delay in the loop to reduce CPU usage

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
