"""
File: blur.py
Name: Brian Chen
-------------------------------
This file shows the original image first,
smiley-face.png, and then compare to its
blurred image. The blur algorithm uses the
average RGB values of a pixel's nearest neighbors.
"""

from simpleimage import SimpleImage


def blur(img):
    """
    :param img: old image
    :return: blurred image
    """
    # instantiate new_img object
    new_img = SimpleImage.blank(img.width, img.height)

    # set initial variables as 0
    red_sum, green_sum, blue_sum, count = 0, 0, 0, 0

    # iterates over the width of image (x starts with 0)
    for x in range(img.width):
        # inter over the height of image (y starts with 0)
        for y in range(img.height):
            # access the neighbor and the adjacent pixels
            # -1 -> pixel on the left/top; 1 -> pixel on the right/bottom
            # start(0, 0) -> check left(-1, 0) and right(1, 0)....end(width-1, 0)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # check if the current neighboring pixel being accessed is within the boundaries of the image
                    if (0 <= x + i < img.width) and (0 <= y + j < img.height):
                        # get pixel from old img
                        old_pixel = img.get_pixel(x + i, y + j)
                        # accumulate rgb sum
                        red_sum += old_pixel.red
                        green_sum += old_pixel.green
                        blue_sum += old_pixel.blue
                        # count only the pixel inside the condition in order to calculate correct neighbor avg.
                        count += 1

            # assign avg. rgb to new img
            new_img.set_rgb(x, y, red_sum // count, green_sum // count, blue_sum // count)

            # reset rgb sum and count
            red_sum, green_sum, blue_sum, count = 0, 0, 0, 0

    return new_img


def main():

    old_img = SimpleImage("images/smiley-face.png")
    old_img.show()

    blurred_img = blur(old_img)
    for i in range(5):
        blurred_img = blur(blurred_img)
    blurred_img.show()


# ---- DO NOT EDIT CODE BELOW THIS LINE ---- #

if __name__ == '__main__':
    main()
