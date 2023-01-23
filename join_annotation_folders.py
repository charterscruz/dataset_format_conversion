'''
Sample Usage:
python join_single_annotation.py

this script converts semantic segmentation (9different annotations for different objects) annotations to binary segmantation
'''

import os
import cv2
import glob
import numpy as np

#todo this should be read as argument and not defined on the code
folder_path = '/media/cruz/data/datasets/marsyn/'

# Define the annotation name. The full name is composed of 3 parts: 
#   1 is a prefix depending on the original image name. I'll call it imgname
imgname = 'Image'

#   2 depends on the class of object. I'll call it objclass
objclass = 'boat'

annotation_name_prefix = imgname + '_' + objclass + '_'


# load each of the annotated images.
images = os.listdir(folder_path)


# todo get number of images
for subfolder_name in os.listdir(folder_path):
    if len(subfolder_name) > 11:
        if subfolder_name[:11] == 'Annotations':
            ssubfolder_list = os.listdir(folder_path + '/' + subfolder_name)
            for ssubfolder_name  in os.listdir(folder_path + '/' + subfolder_name):

                if ssubfolder_name[:11] == 'Annotations':
                    # check existence of a folder called mergedAnnotations
                    isExist = os.path.exists(folder_path + subfolder_name + '/mergedAnnotations' + subfolder_name[11:])
                    if isExist:
                        print('folder: ' + folder_path + subfolder_name + '/mergedAnnotations' + subfolder_name[11:]
                              + ' already exists. Delete folder to proceed')
                        exit()
                    else:
                        os.mkdir(folder_path + subfolder_name + '/mergedAnnotations' + subfolder_name[11:])

                    file_list = os.listdir(folder_path + subfolder_name + '/' + ssubfolder_name)
                    largest_file_number = 0
                    for file_name in file_list:
                        if int(file_name[5:10]) > largest_file_number:
                            largest_file_number = int(file_name[len(imgname):(len(imgname)+5)])
                        print(file_name[len(imgname):(len(imgname)+5)])

                    for img_ctr in range(largest_file_number):
                        print(img_ctr)
                        img_prefix = folder_path + subfolder_name + '/' + ssubfolder_name + '/' + imgname + \
                                    str(str(img_ctr).zfill(5)) + '_' + objclass + '_'
                        instance_list = glob.glob(img_prefix + '*.png')

                        if len(instance_list):
                            cv2.namedWindow('merged_annot', cv2.WINDOW_AUTOSIZE)
                            img_semanticseg = np.zeros_like(cv2.imread(instance_list[0]))
                            cv2.imshow('merged_annot', img_semanticseg)
                            cv2.waitKey(1)

                            for instance_ctr, instance_name in enumerate(instance_list):
                                cv2.namedWindow(str(instance_ctr), cv2.WINDOW_AUTOSIZE)
                                instance_annot = cv2.imread(instance_name)
                                img_semanticseg = img_semanticseg | instance_annot
                                cv2.imshow(str(instance_ctr), instance_annot)
                                cv2.imshow('merged_annot', img_semanticseg)
                                cv2.waitKey(1)

                            cv2.imwrite(folder_path + subfolder_name + '/mergedAnnotations' + subfolder_name[11:] + '/'
                                        + imgname + str(str(img_ctr).zfill(5)) + '_' + objclass + '.png',
                                        img_semanticseg)





cv2.destroyAllWindows()


