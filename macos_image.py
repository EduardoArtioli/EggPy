
import Quartz.CoreGraphics as CG
import cv2
import numpy as np

def capture_screenshot(x, y, width, height):
    region = CG.CGRectMake(x, y, width, height)
    image = CG.CGWindowListCreateImage(region, CG.kCGWindowListOptionOnScreenBelowWindow, CG.kCGNullWindowID, CG.kCGWindowImageDefault)
    if image:
        width = CG.CGImageGetWidth(image)
        height = CG.CGImageGetHeight(image)
        bytes_per_row = CG.CGImageGetBytesPerRow(image)
        pixel_data = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
        image = np.frombuffer(pixel_data, dtype=np.uint8)
        image = image.reshape((height, bytes_per_row//4, 4))
        image = image[:, :width, :]
        # image is scaled due to Retina
        image = cv2.resize(image, (width//2, height//2), interpolation=cv2.INTER_AREA)
        return image
    else:
        # Handle the case where no image is returned
        return None
