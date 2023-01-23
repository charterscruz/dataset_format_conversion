#!/usr/bin/env python
"""
The objective of this script is to look for all image files in a folder and crop several parts of it
and save the cropped areas to file
"""

import sys
import argparse
import glob
import os
import cv2

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_folder",
        help="folder where original images are located"
    )

    parser.add_argument(
        "output_folder",
        help="folder where cropped image will be saved"
    )

    parser.add_argument(
        "cropped_height",
        help="number of lines of the original image (height)"
    )

    parser.add_argument(
        "cropped_width",
        help="number of columns of the original image (width)"
    )

    parser.add_argument(
        "cropped_overlap",
        help="portion of overlap in vertical and horizontal axis during cropping (value 0-1)"
    )

    parser.add_argument(
        "--file_extension",
        nargs='?', default='.jpg', const='.jpg',
        help="folder where original images are located"
    )

    args = parser.parse_args()
    overlap_ratio = float(args.cropped_overlap)
    cropped_width = int(args.cropped_width)
    cropped_height = int(args.cropped_height)
    file_extension = args.file_extension

    # changed to the directory that contains the original images
    os.chdir(args.input_folder)
    # get file list
    image_file_list = glob.glob("*" + file_extension)

    # Create 2 image windows to show the original image and the cropped version
    cv2.namedWindow('full_img', cv2.WINDOW_NORMAL)
    cv2.namedWindow('cropped_img', cv2.WINDOW_NORMAL)

    # Go through all the files in alphabetical order
    for file_ptr in sorted(image_file_list):

        full_image = cv2.imread(args.input_folder + file_ptr)
        [img_height, img_width, _] = full_image.shape
        cv2.imshow('full_img', full_image)

        # number of "windows" in the horizontal axis
        hor_windows = img_width // int((1-overlap_ratio) * cropped_width)
        vert_windows = img_height // int((1-overlap_ratio) * cropped_height)

        # These cycles are ignoring a margin of image that correspond to the remainder of the division
        # of the image width and height by the cropped image size
        for hor_iteration in range(hor_windows-1):
            for vert_iteration in range(vert_windows-1):
                img_crop = full_image[vert_iteration * int((1-overlap_ratio) * cropped_height):
                                      vert_iteration * int((1-overlap_ratio) * cropped_height) + cropped_height,
                                      hor_iteration * int((1-overlap_ratio) * cropped_width):
                                      hor_iteration * int((1-overlap_ratio) * cropped_width) + cropped_width,
                                      :]
                # print position of iteration just to check
                # print('print position of iteration just to check')
                # print(hor_iteration)
                # print(vert_iteration)
                #
                # print(vert_iteration * int(overlap_ratio * cropped_height))
                # print(hor_iteration * int(overlap_ratio * cropped_width))

                # print size of cropped image just to check values
                # print('print size of cropped image just to check values')
                # print(img_crop.shape)

                cv2.imshow('cropped_img', img_crop)

                if cv2.waitKey(1) == 27:
                    # if ESC key is pressed, the entire process is stopped
                    assert 0 == 1, 'ESC key pressed'
                cv2.imwrite(args.output_folder +
                            file_ptr[:-4] + '_' + str(vert_iteration) +
                                       '_' + str(hor_iteration) +
                            file_extension, img_crop)

        print('file_ptr: ', file_ptr)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
