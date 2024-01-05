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
