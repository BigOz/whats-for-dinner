/*
    This program will write image files to a binary, which is one format
    TensorFlow can unpack and use as an image stream. It uses OpenCV to actually
    read in images. It should only be run after the "scale_images.py" and
    "get_image_names.sh" scripts have been run...otherwise, the program will
    still run but spit out a useless, empty binary.

    The program is compiled using cmake and make. Cmake makes things easier by
    automatically linking the libraries needed to call OpenCV from the program.

    I originally tried building the binary in python, but realized python
    doesn't really like it when you try and tell it exactly how many bytes a
    specific value should be, and thus would yield erratic results when writing
    values to the binary file.
*/

#include <iostream>
#include <fstream> //For loading the descriptor file and outputting the bin file
#include <string>
#include <algorithm> //for Randomizing
#include <array> //An array container that can be randomized
#include <random> //Needed for randomizing the inputs
#include <chrono> //Needed for seeding the random engine
#include <opencv2/opencv.hpp> //OpenCV Library

using namespace std;
using namespace cv;

// This is the total quantity of images that will be put into binary files.
// 90% of the files will be placed in a training binary, the remaining 10% will
// be placed in an evaluation binary.
const int QUANTITY = 10000;

// This is the square dimension of each image to be processed.
const int DIMENSION = 32;

int main()
{
    // Opens the stream "input" to bring in the file names
    ifstream input;

    // Imports the list, which was extracted from a previous shell script
    input.open("list.txt");

    // Initializes an array of strings containing file names to be scanned. The
    // container array was used to allow easier randomization using a built in
    // algorithm
    array<string,QUANTITY> files {};

    // Iterates through the list file and saves the file names into the array
    for (int i = 0; i < QUANTITY; ++i)
    {
        getline(input, files[i]);
    }
    // Closes the stream "input"
    input.close();

    // Creates the seed which will be used to randomize the images
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();

    // Shuffles the array of image name strings. This randomization is done to
    // ensure maximun variety when feeding images into the neural net
    shuffle (files.begin(), files.end(), std::default_random_engine(seed));

    // This string contains the relative path to the scaled images.
    string rel_path = "../../images/scaled_images/";

    // Calculates the number of images to be used for training, saving the rest
    // for evaluating.
    int train = QUANTITY * 0.9;

    // Initializes the stream item
    ofstream binfile;

    // Opens the stream, pointing it towards a file names "train.bin." The flag
    // "binary" tells C++ to treat the stream as a binary, which will keep
    // garbage like newlines, etc from being pushed in to it.
    binfile.open("../nn/train.bin", ios::binary);

    // Iterates through the randomized strings, loads the respective image, and
    // processes the type from the filename. The type and image are then written
    // to the binary file.
    for (int i = 0; i < train; ++i)
    {
        // Creates the full path to each file
        string location = rel_path + files[i];

        // Reads the image in as a OpenCV matrix, using the OpenCV function
        // imread()
        Mat image = imread(location);

        // Parses the item name string to determine the item type, which is an
        // integer saved just before the ".JPEG" file extension. Future versions
        // of this script could adapt for different file types.
        string item_type = files[i].substr(files[i].length() - 6, 1);

        // Converts the single-digit string to a uchar type. A uchar is
        // important to ensure a digit is of the appropriate structure for the
        // binary file. Using a signed character type would end up writing
        // the signed bit to the file, which would be a problem when pulling
        // apart the binary later.
        uchar blah = item_type[0] - '0';

        // This is where the item type is actually written to the file. Some
        // important things to note are that the char had to be passed as a
        // pointer, which is why the type is dereferenced and cast into a char*.
        // Also, the size of the uchar has to be passed through, to ensure the
        // appropriate number of bits are written to the file.
        binfile.write((char*) &blah, sizeof(uchar));

        // This section does the writing of each pixel value to the binary
        // file.

        // Iterates through each color layer of the image
        for (int d = 0; d < 3; ++d)
        {
            // Iterates through each row of the image
            for (int i = 0; i < DIMENSION; ++i)
            {
                // Iterates through each column of the image
                for (int j = 0; j < DIMENSION; ++j)
                {
                    // The pixel value is extracted again as a uchar (8 bits).
                    // The Vec3b is needed to tell the program how to read the
                    // 3 layers of the vector. i and j simply refer to the row
                    // and column, while the whole thing needs to include a
                    // reference to d to tell which layer is being accessed.
                    // This value is cast into a uchar.
                    uchar value = (uchar)image.at<Vec3b>(i,j)[d];

                    // Writes the pixel value to the next byte of the binary
                    // image file.
                    binfile.write((char*) &value, sizeof(uchar));
                }
            }
        }
    }
    // Once the loops are complete, the binary file is closed. Assuming a image
    // size of 32 * 32 * 3, and an item type of 1, each record should be
    // 32 * 32 * 3 + 1 bytes long, which means the entire binary file should be
    // exactly QUANTITY * (0.9 * 32 * 32 * 3 + 1) bytes long.
    binfile.close();

    // This section pretty much repeats what was done before, this time writing
    // the remaining images to the evaulation binary. I will only point out
    // important differences.
    ofstream binfile2;

    // This file will be name "eval.bin"
    binfile2.open("../nn/eval.bin", ios::binary);

    // Starts reading images from wherever the previous section finished
    for (int i = train; i < QUANTITY; ++i)
    {
        string location = rel_path + files[i];
        Mat image = imread(location);

        string item_type = files[i].substr(files[i].length() - 6, 1);
        uchar blah = item_type[0] - '0';
        binfile2.write((char*) &blah, sizeof(uchar));

        for (int d = 0; d < 3; ++d)
        {
            for (int i = 0; i < DIMENSION; ++i)
            {
                for (int j = 0; j < DIMENSION; ++j)
                {
                    uchar value = (uchar)image.at<Vec3b>(i,j)[d];
                    binfile2.write((char*) &value, sizeof(uchar));
                }
            }
        }
    }
    binfile2.close();

    return 0;
}
