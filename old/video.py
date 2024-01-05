import cv2 as cv
import numpy as np
import os
from time import time
import pyautogui
from PIL import ImageGrab
from old.vision import Vision 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

vision_drone = Vision('assets/drone/5.jpeg')

vision_drone.init_control_gui()

loop_time = time()
while(True):

  bounding_box = {'top': 1021, 'left': 200, 'width': 1412, 'height': 688}

  screenshot = ImageGrab.grab(bounding_box)
  screenshot = np.array(screenshot)
  screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) # RGB -> BGR
  # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY) # RGB -> BGR
  # screenshot = screenshot[...,:3] # Remove alpha channel
  # screenshot = np.ascontiguousarray(screenshot) # Make it contiguous
  
  rectangles = vision_drone.find(screenshot, 0.5)

  output_image = vision_drone.draw_rectangles(screenshot, rectangles)

  cv.imshow('Matches', output_image)

  print('FPS {}'.format(1 / (time() - loop_time)))
  loop_time = time()


  # Press 'q' to exit
  if cv.waitKey(1) == ord('q'):
    break

cv.destroyAllWindows()
print('Done.')