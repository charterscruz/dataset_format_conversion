import os
import shutil

no_fod_folder = os.listdir('/media/jmbalmeida/Elements/DATASETS/19_dez_cropped/19dez_rpi/cropped/no_fod/')
fod_folder = os.listdir('/media/jmbalmeida/Elements/DATASETS/19_dez_cropped/19dez_rpi/cropped/fod/')
all_images_folder = os.listdir('/media/jmbalmeida/Elements/DATASETS/19_dez_cropped/19dez_rpi/cropped/')

no_fod_folder = set(no_fod_folder)
fod_folder = set(fod_folder)
all_images_folder = set(all_images_folder)

result = all_images_folder - no_fod_folder - fod_folder

print(result)

result1 = list(result)

no_fod_folder = list(no_fod_folder)
fod_folder = list(fod_folder)
all_images_folder = list(all_images_folder)


while all_images_folder == result1:
    shutil.copy2('/media/jmbalmeida/Elements/DATASETS/19_dez_cropped/19dez_rpi/cropped/','/media/jmbalmeida/Elements/DATASETS/19_dez_cropped/19dez_rpi/cropped/test/')

