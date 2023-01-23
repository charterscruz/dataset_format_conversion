#Moves/Copies (change line 33) random images from a folder to another
#Used to generate train, validation and test datasets

import numpy as np
import os
import random
import shutil

#set directories
source_directory = str('/home/ciafa/mnt_point/digits_data/datasets/19dez_rpi_fod_pascal/folder_split/images')
target_directory = str('/home/ciafa/mnt_point/digits_data/datasets/19dez_rpi_fod_pascal/folder_split/images_split/train')
annotations_source_directory = str('/home/ciafa/mnt_point/digits_data/datasets/19dez_rpi_fod_pascal/folder_split/annotations')
annotations_target_directory = str('/home/ciafa/mnt_point/digits_data/datasets/19dez_rpi_fod_pascal/folder_split/annotations_split/train')
data_set_percent_size = float(0.9)

#print(os.listdir(directory))

# list all files in dir that are an image
files = [f for f in os.listdir(source_directory) if f.endswith('.jpg')]

# select a percent of the files randomly 
random_files = random.sample(files, int(len(files)*data_set_percent_size))


# move the randomly selected images by renaming directory 

for random_file_name in random_files:      
    shutil.move(source_directory + '/' + random_file_name, target_directory + '/' + random_file_name)
    continue


# move the relevant labels for the randomly selected images

for image_labels in random_files:
     # strip extension and add .txt to find corellating label file then rename directory.
     shutil.move(annotations_source_directory+'/'+(os.path.splitext(image_labels)[0]+'.xml'), annotations_target_directory+'/'+(os.path.splitext(image_labels)[0]+'.xml'))
     continue
