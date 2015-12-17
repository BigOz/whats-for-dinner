'''
Scales all the images in a folder. The images will be read from one directory,
and renamed in placed in a parallel directory.

Images to be processed should be placed in a folder within the "images"
directory titled "original_images". It is assumed currently the images will be
.JPEG images. Images should be placed in a folder named after whatever the
images are of. So, images of dogs would be placed in their own folder named
"dogs", etc. No other files should be placed in these folders, as they will
cause the program to crash.

After processing, the images will be saved in a folder within the images
directory named "scaled_images". They will be renamed with two numbers,
separated with an underscore. The first number will represent a unique id number
for each image processed. The second number represents the type of whatever the
image is of. The type is extracted from the folder name of the images. The
types are saved into their own file named "items.txt" The first item in the list
is referenced by a "0", the second by "1", etc. up until 9. This file is
generated each time this program is run.
'''

# necessary packages for scaling images
import cv2
# sets the size for the output images (height and width)
IMAGE_SIZE = 32

'''
    This function performs two operations. First, it crops the image to square,
    to prevent images from becoming warped during scaling. Next, it scales the
    image to a square of the dimensions of IMAGE_SIZE. It returns that condensed
    image.
'''
def crop_and_resize( image ):
    # force the image to even dimensions (this makes it easier to crop from the
    # center of the image, and at most loses a single row and column from the
    # original image.
    height = image.shape[0]
    width = image.shape[1]
    image[0:height - (height % 2), 0:width - (width % 2)]

    # square the image
    height = image.shape[0]
    width = image.shape[1]

    # Falling off the end of this if statement means the image was already
    # square to begin with.
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

#Makes sure each image name includes the "type" as an integer
type_counter = 0

#Give each image a unique id, to help in randomizing
image_counter = 0

# Relative location of images. As long as the directory structure is left as-is,
# this should work fine.
image_dir = "../images/original_images/"

#relative location to save to
scale_dir = "../images/scaled_images/"

# A list of the types of objects represented in the images. This will eventually
# be written to a file in the scaled_images directory.
image_types = []

# necessary packages for reading and writing from file system
import os

# Cycles through folder structure and finds each image, applying function and
# saving them to a common folder, with a new name structure. The name structure
# begins with a unique number for every image, followed by a digit representing
# the type of item in the image, as referenced by the "items.txt" file created
# with the scaled images.

# Goes through each image directory
for names in os.listdir(image_dir):

    # Ignores the .gitignore file. THe only reason this file is here in the
    # first place is to ensure an empty directory makes it into the repository.
    if not names.endswith(".gitignore"):

        # Collects the image types
        image_types.append(names)

        #Iterages through each file in the directory
        for images in os.listdir(image_dir + names):

            # Makes sure to only include images
            if images.endswith(".JPEG"):
                print(images)
                image = cv2.imread(image_dir + names + "/" + images)

                # Applies the image transformation
                image = crop_and_resize(image)

                # Writes the image to the scaled_images directory, using the
                # naming scheme as explained.
                cv2.imwrite(scale_dir + str(image_counter) + "_" +
                    str(type_counter) + ".JPEG", image)

                # Increments the counter for each image
                image_counter = image_counter + 1

        # Increments the counter for each image type
        type_counter = type_counter + 1

# Copies the list of found items to a CSV file, to be read in again later when
# building the network of images
import csv
myfile = open(scale_dir + "items.txt", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(image_types)
