'''
    This script outlines a function used to oversegment the 32 * 32 image. I
    never actually ended up using it for anything, because I never got around
    to implementing the saliency map of an image. However, I spent a good amount
    of time playing around with this, so I figured I would still include it.
'''

# import the necessary packages
from skimage.segmentation import slic
from skimage.util import img_as_float
import cv2
import numpy as np

def superpixel_image(image):

    # load the image and convert it to a floating point data type
    image = img_as_float(cv2.imread("../images/scaled_images/10001_9.JPEG"))

    # extracts 100 superpixels from the image. 100 was chosen by simply
    # experimenting with what looked good on a 32 * 32 image. Sigma refers
    # to a gaussian blur that is applied to the image...I've used a small value
    # because my details in my image are so small. OpenCV does not yet have
    # a superpixel method, so I used one from the SciKit Image package.
    superpixels = slic(image, n_segments = 100, sigma = 1)
    return superpixels
