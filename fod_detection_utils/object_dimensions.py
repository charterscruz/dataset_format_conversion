#!/usr/bin/env python
"""
The objective of this script is to look for all image files in a folder and crop several parts of it
and save the cropped areas to file
"""
import csv
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
        "--file_extension",
        nargs='?', default='.jpg', const='.jpg',
        help="folder where original images are located"
    )

    args = parser.parse_args()
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

    f = open('/home/jmbalmeida/Desktop/fod_dimensions_tx2.csv', 'w')

    header = 'image_name, vert_px_top, vert_px_bottom, horiz_px_left, horiz_px_right, height, width'

    f.write(header)

    # load the json file
    labels_var = json.load(open(labels_file))
    for img_counter, _ in enumerate(labels_var):
        # get the name of the image considered in this cycle
        img_name = labels_var[img_counter]['data']['image'][labels_var[img_counter]['data']['image'].find('txway'):]

        print('Loading image: ', img_name)
        # loading image
        full_image = cv2.imread(args.input_folder + img_name)
        # create a copy of the image to allow points to be marked without contaminating the original image
                                                       #full_image_copy = full_image.copy()
        [img_height, img_width, _] = full_image.shape  #[img_height, img_width, _] = full_image_copy.shape

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

            print('FOD coord',  lbl_vert_px_bottom, lbl_vert_px_top, lbl_horiz_px_right, lbl_horiz_px_left)

            fod_height = lbl_vert_px_bottom - lbl_vert_px_top
            fod_width = lbl_horiz_px_right - lbl_horiz_px_left

            print('fod_height = ', fod_height)
            print('fod_width = ', fod_width)

            # header = ['image_name', 'vert_px_top', 'vert_px_bottom', 'horiz_px_left', 'horiz_px,right', 'height',
            #           'width']
            data = str(img_name) + ',' + str(lbl_vert_px_top) + ',' + str(lbl_vert_px_bottom) + ',' + str(lbl_horiz_px_left) + ',' + str(lbl_horiz_px_right) + ',' + str(fod_height) + ',' + str(fod_width) + '\n'

            # with open('/home/jmbalmeida/Desktop/fod_dimensions.csv', 'w', encoding='UTF8', newline='') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(header)

            f.write(data)

            # writer.writerow(data)

        cv2.imshow('full_img_copy', full_image)
        cv2.waitKey(1)
        pass

    f.close()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
