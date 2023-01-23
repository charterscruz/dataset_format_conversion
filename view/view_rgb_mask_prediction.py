#!/usr/bin/env python
"""
The objective of this script is to look for all RGB image files in a folder and check the existence of
manually labelled binary images (ground truth) as well as the segmentation prediction.
If there are the three images, then display them side by side and save the image to folder.
The following is an example of the arguments need to run this script
python view_rgb_mask_prediciton.py
/path/to/folder/rgb
/path/to/folder/mask_gt
/path/to/folder/mask_prediction
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
        "rgb_input_folder",
        help="folder where original images are located"
    )
    parser.add_argument(
        "gt_image_folder",
        help="folder where annotations will be saved"
    )
    parser.add_argument(
        "predictions_folder",
        help="folder where annotations will be saved"
    )


    args = parser.parse_args()
    rgb_input_folder = args.rgb_input_folder
    gt_input_folder = args.gt_image_folder
    # prediction_input_folder = args.gt_image_folder

    # Create 2 image windows to show the original image and the new version
    cv2.namedWindow('img_rgb', cv2.WINDOW_NORMAL)
    cv2.namedWindow('img_gt', cv2.WINDOW_NORMAL)
    cv2.namedWindow('img_prediction', cv2.WINDOW_NORMAL)

    rgb_img_list = os.listdir(rgb_input_folder)

    for img_name in rgb_img_list:
        try:
            cv2.imread(rgb_input_folder+img_name)
            pass
        except cv2.error as e:
            print(e)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)