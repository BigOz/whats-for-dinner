'''
Scales all the images in a folder, while maintaining the same directory
structure
'''
IMAGE_SIZE = 64


# necessary packages for scaling images
import cv2

# load the image and show it
image = cv2.imread("../test/oi/Cabbage/n07714571_10026.JPEG")
cv2.imshow("original", image)
cv2.waitKey(0)
print(image.shape)

# we need to keep in mind aspect ratio so the image does
# not look skewed or distorted -- therefore, we calculate
# the ratio of the new image to the old image
scaling_factor = IMAGE_SIZE / min(image.shape[0], image.shape[1])
print(scaling_factor)
dim = (int(scaling_factor * image.shape[1]), int(scaling_factor * image.shape[0]))
print(dim)

# perform the actual resizing of the image and show it
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("resized", resized)
cv2.waitKey(0)
print(resized.shape)
cv2.imwrite("n07714571_10026.JPEG", resized)
