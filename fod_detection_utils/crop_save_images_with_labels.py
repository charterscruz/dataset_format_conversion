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
    labels_file = args.label_json

    # changed to the directory that contains the original images
    os.chdir(args.input_folder)
    # get file list
    image_file_list = glob.glob("*" + file_extension)

    # Create 2 image windows to show the original image and the cropped version
    cv2.namedWindow('full_img_copy', cv2.WINDOW_NORMAL)
    cv2.namedWindow('full_img', cv2.WINDOW_NORMAL)
    cv2.namedWindow('cropped_img', cv2.WINDOW_NORMAL)

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

        # number of "windows" in the horizontal axis
        hor_windows = img_width // int((1-overlap_ratio) * cropped_width)
        vert_windows = img_height // int((1-overlap_ratio) * cropped_height)

        # These cycles are ignoring a margin of image that correspond to the remainder of the division
        # of the image width and height by the cropped image size
        for hor_iteration in range(hor_windows - 1):
            for vert_iteration in range(vert_windows - 1):
                fod_flag = False
                crop_vert_min = vert_iteration * int((1-overlap_ratio) * cropped_height)
                crop_vert_max = vert_iteration * int((1-overlap_ratio) * cropped_height) + cropped_height
                crop_horiz_min = hor_iteration * int((1-overlap_ratio) * cropped_width)
                crop_horiz_max = hor_iteration * int((1-overlap_ratio) * cropped_width) + cropped_width

                img_crop = full_image[crop_vert_min:crop_vert_max, crop_horiz_min: crop_horiz_max, :]

                # go through each of the annotations of FOD
                for annotation_counter, annotation_var in enumerate(
                        labels_var[img_counter]['annotations'][0]['result']):
                    annotation_points = np.array(annotation_var['value']['points'])
                    lbl_horiz_left, lbl_vert_top = np.min(annotation_points, 0)
                    lbl_horiz_right, lbl_vert_bottom = np.max(annotation_points, 0)

                    # label studio exports the coordinates as a percentagem of image size.
                    # Must convert back to pixel units
                    lbl_vert_px_top = int(lbl_vert_top * img_height / 100)
                    lbl_vert_px_bottom = int(lbl_vert_bottom * img_height / 100)
                    lbl_horiz_px_left = int(lbl_horiz_left * img_width / 100)
                    lbl_horiz_px_right = int(lbl_horiz_right * img_width / 100)

                    # Check if any of the label points is inside the area to crop
                    if crop_vert_min < lbl_vert_px_bottom and crop_vert_max > lbl_vert_px_top and crop_horiz_min < lbl_horiz_px_right and crop_horiz_max > lbl_horiz_px_left:
                        print('there is FOD inside cropped region')
                        print('crop coord', crop_vert_min , crop_vert_max, crop_horiz_min, crop_horiz_max)
                        print('FOD coord',  lbl_vert_px_bottom, lbl_vert_px_top, lbl_horiz_px_right, lbl_horiz_px_left)
                        fod_flag = True
                        break
                        # cv2.imshow('cropped', img_crop)
                        # cv2.imwrite(args.output_folder +
                        #             img_name[:-4] + '_' + str(vert_iteration) +
                        #             '_' + str(hor_iteration) + '_FOD' +
                        #             file_extension, img_crop)
                        #
                        # if cv2.waitKey(10) == 27:
                        #     # if ESC key is pressed, the entire process is stopped
                        #     assert 0 == 1, 'ESC key pressed'

                    else:
                        pass

                if fod_flag:
                    cv2.imshow('cropped', img_crop)
                    #Todo
                    cv2.imwrite(args.output_folder + 'fod/' +
                                img_name[:-4] + '_' + str(vert_iteration) +
                                '_' + str(hor_iteration) + '_FOD' +
                                file_extension, img_crop)
                    # if cv2.waitKey(0) == 27:
                    #     # if ESC key is pressed, the entire process is stopped
                    #     assert 0 == 1, 'ESC key pressed'

                else:
                    cv2.imshow('cropped', img_crop)
                    #Todo
                    cv2.imwrite(args.output_folder + 'no_fod/' +
                                img_name[:-4] + '_' + str(vert_iteration) +
                                '_' + str(hor_iteration) + '_NO_FOD' +
                                file_extension, img_crop)

                    # if cv2.waitKey(1) == 27:
                    #     # if ESC key is pressed, the entire process is stopped
                    #     assert 0 == 1, 'ESC key pressed'

                    # if cv2.waitKey(1) == 27:
                    #     # if ESC key is pressed, the entire process is stopped
                    #     assert 0 == 1, 'ESC key pressed'
                    # cv2.imwrite(args.output_folder +
                    #             img_name[:-4] + '_' + str(vert_iteration) +
                    #             '_' + str(hor_iteration) + '_NO_FOD' +
                    #             file_extension, img_crop)


        # go through each of the annotations of FOD
        for annotation_counter, annotation_var in enumerate(labels_var[img_counter]['annotations'][0]['result']):
            annotation_points = np.array(annotation_var['value']['points'])
            lbl_horiz_left, lbl_vert_top = np.min(annotation_points, 0)
            lbl_horiz_right, lbl_vert_bottom = np.max(annotation_points, 0)

            # label studio exports the coordinates as a percentage of image size. Must convert back to pixel units
            lbl_vert_px_top = int(lbl_vert_top * img_height / 100)
            lbl_vert_px_bottom = int(lbl_vert_bottom * img_height / 100)
            lbl_horiz_px_left = int(lbl_horiz_left * img_width / 100)
            lbl_horiz_px_right = int(lbl_horiz_right * img_width / 100)

            # go through each of the points in each FOD
            for _, annotation_point in enumerate(annotation_points):
                # Draws each of the points as a green point in a copy of the original image
                full_image_copy[int(annotation_point[1]*img_height/100),
                                int(annotation_point[0]*img_width/100), :] = [0, 255, 0]

            # Draws top left and bottom right corners of a bounding box that would contain every labeled points as
            # thicker yellow point
            full_image_copy[lbl_vert_px_top:lbl_vert_px_top+3, lbl_horiz_px_left:lbl_horiz_px_left+3, :] = [0, 255, 255]
            full_image_copy[lbl_vert_px_bottom:lbl_vert_px_bottom+3, lbl_horiz_px_right:lbl_horiz_px_right+3, :] = [0, 255, 255]

        cv2.imshow('full_img_copy', full_image_copy)
        cv2.waitKey(1)
        pass

    # Go through all the files in alphabetical order
    for file_ptr in sorted(image_file_list):

        repeated_name = False

        for img_counter, _ in enumerate(labels_var):
            # get the name of the image considered in this cycle
            img_name = labels_var[img_counter]['data']['image'][labels_var[img_counter]['data']['image'].find('txway'):]

            if img_name == file_ptr:
                # print('img_name: ', img_name)
                # print('file_ptr: ', file_ptr)
                repeated_name = True

        if repeated_name:
            pass

        else:

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

                    #     # if ESC key is pressed, the entire process is stopped
                    #     assert 0 == 1, 'ESC key pressed'
        #             cv2.imwrite(args.output_folder + 'no_fod/' +
        #                             img_name[:-4] + '_' + str(vert_iteration) +
        #                             '_' + str(hor_iteration) + '_NO_FOD' +
        #                             file_extension, img_crop)
        # #             # cv2.imshow('cropped_img', img_crop)
        # #             #
        # #             #     # if ESC key is pressed, the entire process is stopped
        # #             #     assert 0 == 1, 'ESC key pressed'
        #             cv2.imwrite(args.output_folder + 'no_fod/' +
        #                                 img_name[:-4] + '_' + str(vert_iteration) +
        #                                 '_' + str(hor_iteration) + '_NO_FOD' +
        #                                 file_extension, img_crop)
        #             # if cv2.waitKey(1) == 27:
        #             #     # if ESC key is pressed, the entire process is stopped
        #             #     assert 0 == 1, 'ESC key pressed'

                    cv2.imwrite(args.output_folder + 'no_fod/' +
                                file_ptr[:-4] + '_' + str(vert_iteration) +
                                           '_' + str(hor_iteration) + '_NO_FOD' +
                                            file_extension, img_crop)

        #     # print('file_ptr: ', file_ptr)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
