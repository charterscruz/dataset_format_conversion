#!/usr/bin/env python
"""
The objective of this script is to look for all image files in a folder and convert the Label studio annotation into a
binary mask. The binary mask will be saved as a png image
The following is an example of the arguments need to run this script
python transform_LsJson_binaryMask.py
/path/to/folder/19dez_tx2_fod/
/path/to/folder//19dez_tx2.json
/path/to/folder/cropped_for_segmentation/550/images/
/path/to/folder/cropped_for_segmentation/550/masks/
550
550
0.1

"""

import sys
import argparse
import os
import cv2
import json
import numpy as np


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_folder",
        help="folder where original images are located"
    )
    parser.add_argument(
        "label_json",
        help="json file with the labelling project data"
    )

    parser.add_argument(
        "images_output_folder",
        help="folder where annotations will be saved"
    )

    parser.add_argument(
        "annotation_output_folder",
        help="folder where annotations will be saved"
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
    labels_file = args.label_json

    # changed to the directory that contains the original images
    os.chdir(args.input_folder)

    # Create 2 image windows to show the original image and the new version
    cv2.namedWindow('full_img_copy', cv2.WINDOW_NORMAL)
    cv2.namedWindow('full_img', cv2.WINDOW_NORMAL)
    cv2.namedWindow('cropped_img', cv2.WINDOW_NORMAL)
    cv2.namedWindow('cropped_bin_img', cv2.WINDOW_NORMAL)

    # load the json file
    labels_var = json.load(open(labels_file))
    for img_counter, _ in enumerate(labels_var):
        # get the name of the image considered in this cycle
        img_name = labels_var[img_counter]['data']['image'][labels_var[img_counter]['data']['image'].find('image'):]

        print('Loading image: ', img_name)
        # loading image
        full_image = cv2.imread(args.input_folder + img_name)
        # create a copy of the image to allow points to be marked without contaminating the original image
        full_image_copy = full_image.copy()
        [img_height, img_width, _] = full_image_copy.shape

        for annotation_counter, annotation_var in enumerate(labels_var[img_counter]['annotations'][0]['result']):
            annotation_points = np.array(annotation_var['value']['points'])

            annotation_points_absolute = np.multiply(annotation_points,
                                                     np.tile([img_width / 100, img_height/100],
                                                             (annotation_points.shape[0],1)))

            bin_image = np.zeros_like(full_image_copy)
            cv2.fillPoly(bin_image, [np.int32(annotation_points_absolute)], [255, 255, 255])

            # go through each of the points in each FOD
            for _, annotation_point in enumerate(annotation_points):
                # Draws each of the points as a green point in a copy of the original image
                # full_image_copy[int(annotation_point[1] * img_height / 100),
                # int(annotation_point[0] * img_width / 100), :] = [0, 255, 0]
                pass

        # show the images
        cv2.imshow('full_img_copy', full_image_copy)
        cv2.imshow('full_img', bin_image)

        # Crop the rgb image and the mask
        # These cycles are ignoring a margin of image that correspond to the remainder of the division
        # of the image width and height by the cropped image size

        # number of "windows" in the horizontal axis
        hor_windows = img_width // int((1 - overlap_ratio) * cropped_width)
        vert_windows = img_height // int((1 - overlap_ratio) * cropped_height)

        for hor_iteration in range(hor_windows - 1):
            print('hor_iteration: ', hor_iteration)
            for vert_iteration in range(vert_windows - 1):
                print('___vert_iteration: ', vert_iteration)
                crop_vert_min = vert_iteration * int((1 - overlap_ratio) * cropped_height)
                crop_vert_max = vert_iteration * int((1 - overlap_ratio) * cropped_height) + cropped_height
                crop_horiz_min = hor_iteration * int((1 - overlap_ratio) * cropped_width)
                crop_horiz_max = hor_iteration * int((1 - overlap_ratio) * cropped_width) + cropped_width

                cropped_image = full_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]
                cropped_bin_image = bin_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]

                cv2.imshow('cropped_img', cropped_image)
                cv2.imshow('cropped_bin_img', cropped_bin_image)
                cv2.waitKey(1)

                cv2.imwrite(args.images_output_folder + img_name[:-4] + '_' + str(hor_iteration) + '_' +
                            str(vert_iteration) + '.png', cropped_image)
                cv2.imwrite(args.annotation_output_folder + img_name[:-4] + '_' + str(hor_iteration) + '_' +
                            str(vert_iteration) + '.png', cropped_bin_image)

            # account for the vertical remainder of image when applying tilling
            print('___vert_iteration: ', vert_iteration + 1)
            crop_vert_min = img_height - cropped_height
            crop_vert_max = img_height
            crop_horiz_min = hor_iteration * int((1 - overlap_ratio) * cropped_width)
            crop_horiz_max = hor_iteration * int((1 - overlap_ratio) * cropped_width) + cropped_width
            cropped_image = full_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]
            cropped_bin_image = bin_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]

            cv2.imshow('cropped_img', cropped_image)
            cv2.imshow('cropped_bin_img', cropped_bin_image)
            cv2.waitKey(1)

            cv2.imwrite(args.images_output_folder + img_name[:-4] + '_' + str(hor_iteration) + '_' +
                        str(vert_iteration + 1) + '.png', cropped_image)
            cv2.imwrite(args.annotation_output_folder + img_name[:-4] + '_' + str(hor_iteration) + '_' +
                        str(vert_iteration +1) + '.png', cropped_bin_image)

        print('horiz_iteration: ', hor_iteration + 1)

        for vert_iteration in range(vert_windows - 1):
            print('___vert_iteration: ', vert_iteration)

            crop_vert_min = vert_iteration * int((1 - overlap_ratio) * cropped_height)
            crop_vert_max = vert_iteration * int((1 - overlap_ratio) * cropped_height) + cropped_height
            crop_horiz_min = img_width - cropped_width
            crop_horiz_max = img_width

            cropped_image = full_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]
            cropped_bin_image = bin_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]

            cv2.imshow('cropped_img', cropped_image)
            cv2.imshow('cropped_bin_img', cropped_bin_image)
            cv2.waitKey(1)

            cv2.imwrite(args.images_output_folder + img_name[:-4] + '_' + str(hor_iteration+1) + '_' +
                        str(vert_iteration) + '.png', cropped_image)
            cv2.imwrite(args.annotation_output_folder + img_name[:-4] + '_' + str(hor_iteration+1) + '_' +
                        str(vert_iteration) + '.png', cropped_bin_image)

            print('___vert_iteration: ', vert_iteration + 1)
            crop_vert_min = img_height - cropped_height
            crop_vert_max = img_height
            crop_horiz_min = img_width - cropped_width
            crop_horiz_max = img_width

            cropped_image = full_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]
            cropped_bin_image = bin_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]

            cv2.imshow('cropped_img', cropped_image)
            cv2.imshow('cropped_bin_img', cropped_bin_image)
            cv2.waitKey(1)

            cv2.imwrite(args.images_output_folder + img_name[:-4] + '_' + str(hor_iteration+1) + '_' +
                        str(vert_iteration + 1) + '.png', cropped_image)
            cv2.imwrite(args.annotation_output_folder + img_name[:-4] + '_' + str(hor_iteration+1) + '_' +
                        str(vert_iteration + 1) + '.png', cropped_bin_image)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)