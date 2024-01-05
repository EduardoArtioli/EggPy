import cv2
from defines import *
from PIL import Image

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
    img_grey = apply_ignore_areas(img_grey)
    img_masked = cv2.inRange(img_grey, THRESHOLD_LOW, THRESHOLD_HIGH)
    return Image.fromarray(img_masked)

def draw_debug_image(img):
    img = draw_ignored_areas(img)
    cv2.imshow("Drone Catcher", img)