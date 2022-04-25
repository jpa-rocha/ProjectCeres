import time
import picamera
import cv2
import numpy as np
from fastiecm import fastiecm

def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)
    shape = image.shape
    height = int(shape[0] / 4)
    width = int(shape[1] / 4)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi

def ndvi_full(image, string):
	contrasted = contrast_stretch(image)
	ndvi = calc_ndvi(contrasted)
	ndvi_contrasted = contrast_stretch(ndvi)
	color_mapped_prep = ndvi_contrasted.astype(np.uint8)
	color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
	#display(color_mapped_image, 'Color mapped')
	cv2.imwrite(string, color_mapped_image)

with picamera.PiCamera() as camera:
	camera.resolution = (1280, 720)
	camera.vflip = 1
	camera.start_preview()
	time.sleep(1)
	for i, picture in enumerate(camera.capture_continuous('pictures_test/image{counter:02d}.jpg')):
		print('Captured image %s' %picture)
		string = f"pictures_contrasted/image{i:02d}.jpg"
		image = cv2.imread(picture)
		ndvi_full(image, string)
		if i == 100:
			break
		time.sleep(60)
	camera.stop_preview()

