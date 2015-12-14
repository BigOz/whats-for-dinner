'''
Scales all the images in a folder, while maintaining the same directory
structure
'''

# necessary packages for scaling images
import cv2
# sets the size of the output images (height and width)
IMAGE_SIZE = 64

'''
    This function performs two operations. First, it crops the image to square,
    to prevent images from becoming warped. Next, it scales the image to a
    square of the dimensions of IMAGE_SIZE. It returns that condensed image.
'''
def crop_and_resize( image ):
    # force the image to even dimensions (this makes it easier to crop)
    height = image.shape[0]
    width = image.shape[1]
    image[0:height - (height % 2), 0:width - (width % 2)]

    # square the image
    height = image.shape[0]
    width = image.shape[1]
    if height < width:
        difference = (width - height) / 2
        image = image[0:height, difference:width - difference]
    elif height > width:
        difference = (height - width) / 2
        image = image[difference:height - difference, 0:height]

    # resizes the image to the dimensions of IMAGE_SIZE
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE),
        interpolation = cv2.INTER_AREA)
    return image

# counter for naming files
type_counter = 0 #Makes sure each image name includes the "type" as an integer
image_counter = 0 #Give each image a unique id, to help in randomizing
image_dir = "../images/original_images/" #relative location of images
scale_dir = "../images/scaled_images/" #relative location to save to
image_types = [] #a list of the types of objects represented in the images

# necessary packages for reading and writing from file system
import os

# Cycles through folder structure and finds each image, applying function and
# saving them to a common folder, with a new name structure. The name structure
# begins with a unique number for every image, followed by a digit representing
# the type of item in the image, as referenced by the "items.txt" file created
# with the scaled images.
for names in os.listdir(image_dir): #Goes through each image directory
    if not names.endswith(".gitignore"): #ignores the .gitignore file
        image_types.append(names)
        for images in os.listdir(image_dir + names): #each file in the directory
            if images.endswith(".JPEG"): #makes sure to only include images
                print(images)
                image = cv2.imread(image_dir + names + "/" + images)
                image = crop_and_resize(image) #applies the function above
                cv2.imwrite(scale_dir + str(image_counter) + "_" +
                    str(type_counter) + ".JPEG", image)
                image_counter = image_counter + 1
        type_counter = type_counter + 1

# Copies the list of found items to a CSV file, to be read in again later when
# building the network of images
import csv
myfile = open(scale_dir + "items.txt", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(image_types)
