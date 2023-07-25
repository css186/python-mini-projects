"""
File: stanCodoshop.py
Name: Brian Chen
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue) -> int:
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    return ((pixel.red - red) ** 2 + (pixel.green - green) ** 2 + (pixel.blue - blue) ** 2) ** 0.5


def get_average(pixels) -> list:
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    # set starting value equals 0
    red, green, blue = 0, 0, 0

    # loop for each pixel and increment starting value by each pixel color value
    for pixel in pixels:
        red += pixel.red
        green += pixel.green
        blue += pixel.blue

    # calculate the average
    red = red // len(pixels)
    green = green // len(pixels)
    blue = blue // len(pixels)

    return [red, green, blue]


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    # get average values from pixel list
    averages = get_average(pixels)

    # create a list to store a tuple containing each pixel and the distance between its average RGB -> (pixel, dist)
    pixel_list = [(pixel, get_pixel_dist(pixel, averages[0], averages[1], averages[2])) for pixel in pixels]

    # get the pixel tuple with the smallest distance(by passing the second element as key)
    # once get the smallest tuple, return the pixel(the first element)
    return min(pixel_list, key=lambda element: element[1])[0]


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    
    # ----- YOUR CODE STARTS HERE ----- #
    # Write code to populate image and create the 'ghost' effect
    # Test Code
    # green_pixel = SimpleImage.blank(20, 20, "green").get_pixel(0, 0)
    # red_pixel = SimpleImage.blank(20, 20, "red").get_pixel(0, 0)
    # blue_pixel = SimpleImage.blank(20, 20, "blue").get_pixel(0, 0)
    # best1 = get_best_pixel([green_pixel, blue_pixel, blue_pixel])
    # print(best1.red, best1.green, best1.blue)

    # iterate all the pixels in an image
    for i in range(width):
        for j in range(height):
            # find the best pixel
            best_pixel = get_best_pixel(list(map(lambda image: image.get_pixel(i, j), images)))
            # add to the blank image
            result.set_rgb(i, j, best_pixel.red, best_pixel.green, best_pixel.blue)

    # ----- YOUR CODE ENDS HERE ----- #

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
